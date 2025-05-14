page 50114 "Machine Types"
{
    PageType = List;
    SourceTable = "Machine Type";
    ApplicationArea = All;
    UsageCategory = Lists;
    Caption = 'Machine Types';

    layout
    {
        area(content)
        {
            repeater(Group)
            {
                field("Machine Type ID"; Rec."Machine Type ID")
                {
                    ApplicationArea = All;
                }
            }
        }
    }
}