page 50124 "Machine Component Risk"
{
    PageType = List;
    ApplicationArea = All;
    SourceTable = "Machine Component Assessment";

    layout
    {
        area(content)
        {
            repeater(Group)
            {
                field("Machine ID"; Rec."Machine ID") { ApplicationArea = All; }
                field("Machine Type"; Rec."Machine Type") { ApplicationArea = All; }
                field("Component"; Rec."Component") { ApplicationArea = All; }
                field("Predicted RUL (hrs)"; Rec."Predicted RUL (mins)") { ApplicationArea = All; }
                field("Risk Level"; Rec."Risk Level") { ApplicationArea = All; }
                field("Assessment Date"; Rec."Assessment Date") { ApplicationArea = All; }
            }
        }
    }
}
