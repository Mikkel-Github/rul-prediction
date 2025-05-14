page 50120 "Log Maintenance Event"
{
    PageType = StandardDialog;
    ApplicationArea = All;
    Caption = 'Log Maintenance Event';

    layout
    {
        area(content)
        {
            group(Group)
            {
                field("Machine ID"; MachineIDInput)
                {
                    ApplicationArea = All;

                    trigger OnLookup(var Text: Text): Boolean
                    var
                        MachineRec: Record "Machine";
                    begin
                        if Page.RunModal(Page::"Machines", MachineRec) = Action::LookupOK then begin
                            MachineIDInput := MachineRec."Machine ID";
                            Text := MachineIDInput;
                            exit(true);
                        end;
                        exit(false);
                    end;
                }

                field("Active Time"; ActiveTimeInput) { ApplicationArea = All; }
                field("Fault Type"; ComponentTypeInput)
                {
                    ApplicationArea = All;
                    ToolTip = 'Select or type a new component type';
                    TableRelation = "Machine Component"."Component Name ID";
                    AssistEdit = true;
                    Enabled = (EventTypeInput = EventTypeInput::Failure) or (EventTypeInput = EventTypeInput::PreemptiveReplacement);
                }
                // field("Repair/Replace Type"; RepairReplaceTypeInput) { ApplicationArea = All; }
                field("Cost"; CostInput) { ApplicationArea = All; }
                field("Event Type"; EventTypeInput) { ApplicationArea = All; }
            }
        }
    }

    var
        MachineIDInput: Code[20];
        ActiveTimeInput: Integer;
        ComponentTypeInput: Text[100];
        // RepairReplaceTypeInput: Text[100];
        CostInput: Decimal;
        EventTypeInput: Enum "Maintenance Event Type";
        ComponentTypeRec: Record "Machine Component";

    trigger OnQueryClosePage(CloseAction: Action): Boolean
    var
        NewEvent: Record "Maintenance Event";
    begin
        if CloseAction = Action::OK then begin
            if MachineIDInput = '' then
                Error('Please select a Machine ID.');
            if ((EventTypeInput = EventTypeInput::Failure) or (EventTypeInput = EventTypeInput::PreemptiveReplacement)) and (ComponentTypeInput = '') then
                Error('Please provide a fault.');

            if not (ComponentTypeInput = '') then begin
                // Create machine component type if it doesn't exist
                if ComponentTypeRec.FindFirst() then begin
                    ComponentTypeRec.SetRange("Component Name ID", ComponentTypeInput);
                    if ComponentTypeRec.FindFirst() then
                        ComponentTypeInput := ComponentTypeRec."Component Name ID"
                    else begin
                        ComponentTypeRec.Init();
                        ComponentTypeRec."Component Name ID" := ComponentTypeInput;
                        ComponentTypeRec.Insert();
                    end;
                end;
            end;


            NewEvent.Init();
            NewEvent."Machine ID" := MachineIDInput;
            NewEvent."Active Time" := ActiveTimeInput;
            if ((EventTypeInput = EventTypeInput::Failure) or (EventTypeInput = EventTypeInput::PreemptiveReplacement)) then
                NewEvent."Fault Type" := ComponentTypeInput;
            // NewEvent."Repair/Replace Type" := RepairReplaceTypeInput;
            NewEvent."Cost" := CostInput;
            NewEvent."Event Type" := EventTypeInput;
            NewEvent.Insert();

            Message('Maintenance Event logged for machine "%1".', MachineIDInput);
        end;

        exit(true);
    end;
}
