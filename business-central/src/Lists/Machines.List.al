page 50100 "Machines"
{
    PageType = List;
    SourceTable = "Machine";
    ApplicationArea = All;
    UsageCategory = Lists;
    Caption = 'Machines';

    layout
    {
        area(content)
        {
            repeater(Group)
            {
                field("Machine ID"; Rec."Machine ID")
                {
                    ApplicationArea = All;
                }
                field("Machine Type"; Rec."Machine Type")
                {
                    ApplicationArea = All;
                }
            }
        }
    }
}