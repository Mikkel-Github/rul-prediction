page 50115 "Machine Component"
{
    PageType = List;
    SourceTable = "Machine Component";
    ApplicationArea = All;
    UsageCategory = Lists;
    Caption = 'Machine Component';

    layout
    {
        area(content)
        {
            repeater(Group)
            {
                field("Component Name ID"; Rec."Component Name ID")
                {
                    ApplicationArea = All;
                }
            }
        }
    }
}