page 50134 "Schedule Input Dialog"
{
    PageType = StandardDialog;
    Caption = 'Schedule Maintenance';
    ApplicationArea = All;

    layout
    {
        area(content)
        {
            group(General)
            {
                field(StartDateTime; StartDateTime)
                {
                    ApplicationArea = All;
                    Caption = 'Start Date & Time';
                }
                field(EndDateTime; EndDateTime)
                {
                    ApplicationArea = All;
                    Caption = 'End Date & Time';
                }
            }
        }
    }

    var
        StartDateTime: DateTime;
        EndDateTime: DateTime;

    procedure GetStart(): DateTime
    begin
        exit(StartDateTime);
    end;

    procedure GetEnd(): DateTime
    begin
        exit(EndDateTime);
    end;
}
