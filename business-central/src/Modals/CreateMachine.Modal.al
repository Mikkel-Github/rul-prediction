page 50130 "Create Machine"
{
    PageType = StandardDialog;
    ApplicationArea = All;
    Caption = 'Create Machine';

    layout
    {
        area(content)
        {
            group(Group)
            {
                field("Machine ID"; MachineIDInput)
                {
                    ApplicationArea = All;
                }
                field("Machine Type"; MachineTypeInput)
                {
                    ApplicationArea = All;
                    ToolTip = 'Select or type a new machine type';
                    TableRelation = "Machine Type"."Machine Type ID";
                    AssistEdit = true;
                }
            }
        }
    }

    var
        MachineIDInput: Code[20];
        MachineTypeInput: Code[20];

    trigger OnOpenPage()
    begin
        // Auto-generate machine ID when the page is opened
        MachineIDInput := GetNextMachineID();
    end;

    trigger OnQueryClosePage(CloseAction: Action): Boolean
    var
        NewMachine: Record "Machine";
        MachineTypeRec: Record "Machine Type";
    begin
        if CloseAction = Action::OK then begin
            if (MachineIDInput = '') or (MachineTypeInput = '') then begin
                Error('Please fill in both Machine ID and Machine Type.');
            end;

            if NewMachine.Get(MachineIDInput) then
                Error('Machine ID "%1" already exists.', MachineIDInput);


            // Create machine type if it doesn't exist
            if MachineTypeRec.FindFirst() then begin
                MachineTypeRec.SetRange("Machine Type ID", MachineTypeInput);
                if MachineTypeRec.FindFirst() then
                    MachineTypeInput := MachineTypeRec."Machine Type ID" // use original casing
                else begin
                    MachineTypeRec.Init();
                    MachineTypeRec."Machine Type ID" := MachineTypeInput;
                    MachineTypeRec.Insert();
                end;
            end;

            NewMachine.Init();
            NewMachine."Machine ID" := MachineIDInput;
            NewMachine."Machine Type" := MachineTypeInput;
            NewMachine.Insert();

            Message('Machine "%1" created.', MachineIDInput);
        end;

        exit(true); // allow page to close
    end;

    // Function to get the next Machine ID
    local procedure GetNextMachineID(): Code[20]
    var
        MachineRec: Record "Machine";
        NewID: Integer;
    begin
        NewID := 1;

        if not MachineRec.IsEmpty then begin
            NewID := MachineRec.Count + 1;
        end;

        exit(Format(NewID));
    end;
}