table 50103 "Machine Schedule"
{
    DataClassification = ToBeClassified;

    fields
    {
        field(1; "Schedule ID"; Code[20])
        {
            DataClassification = SystemMetadata;
            Caption = 'Schedule ID';
        }
        field(2; "Machine ID"; Code[20])
        {
            DataClassification = ToBeClassified;
            Caption = 'Machine ID';
            TableRelation = "Machine"."Machine ID";
        }
        field(3; "Component"; Text[100])
        {
            Caption = 'Component';
        }
        field(4; "Start Date"; DateTime)
        {
            Caption = 'Start Date & Time';
            DataClassification = ToBeClassified;
        }
        field(5; "End Date"; DateTime)
        {
            Caption = 'End Date & Time';
            DataClassification = ToBeClassified;
        }
        field(6; "Event Type"; Enum "Schedule Event Type")
        {
            DataClassification = ToBeClassified;
        }
    }

    keys
    {
        key(PK; "Schedule ID")
        {
            Clustered = true;
        }
    }
}
