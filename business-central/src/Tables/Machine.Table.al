table 50100 "Machine"
{
    Caption = 'Machine';
    DataClassification = ToBeClassified;

    fields
    {
        field(1; "Machine ID"; Code[20])
        {
            Caption = 'Machine ID';
            DataClassification = CustomerContent;
        }

        field(2; "Machine Type"; Text[50])
        {
            Caption = 'Machine Type';
            DataClassification = ToBeClassified;
        }
    }

    keys
    {
        key(PK; "Machine ID")
        {
            Clustered = true;
        }
    }
}
