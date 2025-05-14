enum 50100 "Maintenance Event Type"
{
    Extensible = false;

    value(0; Service)
    {
        Caption = 'Service';
    }
    value(1; Failure)
    {
        Caption = 'Failure';
    }
    value(2; PreemptiveReplacement)
    {
        Caption = 'Preemptive Replacement';
    }
}
