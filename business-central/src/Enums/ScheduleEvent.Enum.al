enum 50101 "Schedule Event Type"
{
    Extensible = true;

    value(0; "Rental") { Caption = 'Rental'; }
    value(1; "Service") { Caption = 'Service'; }
    value(2; PreemptiveReplacement)
    {
        Caption = 'Preemptive Replacement';
    }
}
