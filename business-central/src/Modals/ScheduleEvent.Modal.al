page 50121 "Add Schedule Entry"
{
    PageType = StandardDialog;
    Caption = 'Add Rental or Service';
    ApplicationArea = All;

    layout
    {
        area(content)
        {
            group("Rental Details")
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
                field(StartDateInput; StartDateInput) { ApplicationArea = All; }
                field(EndDateInput; EndDateInput) { ApplicationArea = All; }
                field(EventTypeInput; EventTypeInput) { ApplicationArea = All; }
            }
        }
    }

    var
        MachineIDInput: Code[20];
        StartDateInput: DateTime;
        EndDateInput: DateTime;
        EventTypeInput: Enum "Schedule Event Type";

    trigger OnQueryClosePage(CloseAction: Action): Boolean
    var
        NewEntry: Record "Machine Schedule";
    begin
        if CloseAction = Action::OK then begin
            if MachineIDInput = '' then
                Error('Machine ID is required.');

            NewEntry.Init();
            NewEntry."Schedule ID" := (NewEntry.Count + 1).ToText();
            NewEntry."Machine ID" := MachineIDInput;
            NewEntry."Start Date" := StartDateInput;
            NewEntry."End Date" := EndDateInput;
            NewEntry."Event Type" := EventTypeInput;
            NewEntry.Insert();

            Message('Schedule entry created.');
        end;
        exit(true);
    end;
}
