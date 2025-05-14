page 50140 "Machine Schedule Calendar"
{
    PageType = ListPart;
    SourceTable = "Machine Schedule";
    ApplicationArea = All;
    Caption = 'Machine Schedule Calendar';

    layout
    {
        area(content)
        {
            repeater(Group)
            {
                //field("Schedule ID"; Rec."Schedule ID") { ApplicationArea = All; }
                field("Machine ID"; Rec."Machine ID") { ApplicationArea = All; Width = 1; }
                field("Component"; Rec."Component") { ApplicationArea = All; Width = 10; }
                field("Start Date"; Rec."Start Date") { ApplicationArea = All; Width = 8; }
                field("End Date"; Rec."End Date") { ApplicationArea = All; Width = 8; }
                field("Event Type"; Rec."Event Type") { ApplicationArea = All; }
            }
        }
    }
}
