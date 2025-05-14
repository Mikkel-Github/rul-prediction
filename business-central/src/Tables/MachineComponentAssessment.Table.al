table 50120 "Machine Component Assessment"
{
    DataClassification = ToBeClassified;

    fields
    {
        field(1; "Machine ID"; Code[20]) { TableRelation = "Machine"."Machine ID"; }

        field(2; "Machine Type"; Text[50])
        {
            DataClassification = CustomerContent;
        }

        field(3; "Component"; Text[50])
        {
            DataClassification = CustomerContent;
        }

        field(4; "Predicted RUL (mins)"; Decimal)
        {
            DataClassification = CustomerContent;
        }

        field(5; "Risk Level"; Enum "Risk Level")
        {
            Caption = 'Risk Level';
        }

        field(6; "Assessment Date"; DateTime)
        {
            DataClassification = SystemMetadata;
        }

        field(7; "Entry ID"; Integer)
        {
            AutoIncrement = true;
            DataClassification = SystemMetadata;
        }
    }

    keys
    {
        key(PK; "Entry ID") { Clustered = true; }
        key(MachineComponent; "Machine ID", "Component") { }
    }

    trigger OnInsert()
    begin
        "Assessment Date" := CurrentDateTime();
    end;
}
