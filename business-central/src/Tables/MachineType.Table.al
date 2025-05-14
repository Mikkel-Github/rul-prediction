table 50102 "Machine Type"
{
    Caption = 'Machine Type';
    DataClassification = ToBeClassified;

    fields
    {
        field(1; "Machine Type ID"; Code[50])
        {
            Caption = 'Machine Type';
        }
    }

    keys
    {
        key(PK; "Machine Type ID") { Clustered = true; }
    }
}
