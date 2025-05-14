table 50101 "Maintenance Event"
{
    DataClassification = ToBeClassified;

    fields
    {
        field(1; "Entry No."; Integer)
        {
            AutoIncrement = true;
            DataClassification = SystemMetadata;
        }
        field(2; "Machine ID"; Code[20]) { TableRelation = "Machine"."Machine ID"; }
        field(3; "Active Time"; Integer) { }
        field(4; "Fault Type"; Text[50]) { }
        // field(5; "Repair/Replace Type"; Text[50]) { }
        field(6; "Cost"; Decimal) { }
        field(7; "Event Type"; Enum "Maintenance Event Type") { Caption = 'Event Type'; }
    }

    keys { key(PK; "Entry No.") { Clustered = true; } }
}
