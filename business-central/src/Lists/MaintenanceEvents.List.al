page 50101 "Maintenance Events"
{
    PageType = List;
    SourceTable = "Maintenance Event";
    UsageCategory = Administration;
    ApplicationArea = All;
    Caption = 'Maintenance events';

    layout
    {
        area(content)
        {
            repeater(Group)
            {
                field("Machine ID"; Rec."Machine ID") { }
                field("Active Time"; Rec."Active Time") { }
                field("Fault Type"; Rec."Fault Type") { }
                // field("Repair/Replace Type"; Rec."Repair/Replace Type") { }
                field("Cost"; Rec."Cost") { }
                field("Event Type"; Rec."Event Type") { }
            }
        }
    }

    actions
    {
        area(processing)
        {
            action("Send to API")
            {
                ApplicationArea = All;
                trigger OnAction()

                var
                    Client: HttpClient;
                    Content: HttpContent;
                    Json: JsonObject;
                    Response: HttpResponseMessage;
                    JsonText: Text;
                    Headers: HttpHeaders;
                begin
                    Json.Add('machine_id', Rec."Machine ID");
                    Json.Add('active_time', Rec."Active Time");
                    Json.Add('fault_type', Rec."Fault Type");
                    // Json.Add('repair_replace_type', Rec."Repair/Replace Type");
                    Json.Add('cost', Rec.Cost);
                    Json.Add('event_type', Format(Rec."Event Type"));

                    Json.WriteTo(JsonText);
                    Content.WriteFrom(JsonText);
                    Headers.Add('Content-Type', 'application/json');
                    Client.Post('URL', Content, Response);
                    Message('Sent to backend.');
                end;
            }
        }
    }
}
