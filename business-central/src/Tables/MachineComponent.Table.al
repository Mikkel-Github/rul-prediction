table 50105 "Machine Component"
{
    DataClassification = CustomerContent;

    fields
    {
        field(2; "Component Name ID"; Text[50])
        {
            DataClassification = CustomerContent;
            Caption = 'Component Name';
        }
    }

    keys
    {
        key(PK; "Component Name ID") { Clustered = true; }
    }
}
