page 50110 "Predictive Maintenance Hub"
{
    PageType = ListPlus;
    ApplicationArea = All;
    UsageCategory = Administration;
    Extensible = true;

    layout
    {
        area(FactBoxes)
        {

        }
        area(content)
        {
            group("Dashboard Overview")
            {
                Caption = 'Predictive Maintenance Dashboard';

                group("Summary Tiles")
                {
                    ShowCaption = false;
                    grid(Info)
                    {
                        group("Data Information")
                        {
                            field("Total Machines"; TotalMachines)
                            {
                                ApplicationArea = All;
                                Editable = false;
                            }
                            field("Total Events"; TotalEvents)
                            {
                                ApplicationArea = All;
                                Editable = false;
                            }
                        }
                        group("Risk Counts for Components")
                        {
                            field("High-Risk"; HighRiskCount)
                            {
                                ApplicationArea = All;
                                Editable = false;
                            }
                            field("Medium-Risk"; MediumRiskCount)
                            {
                                ApplicationArea = All;
                                Editable = false;
                            }
                        }
                        field("Last Prediction Run"; LastPredictionDate)
                        {
                            ApplicationArea = All;
                            Editable = false;
                        }
                    }
                }
            }

            group("Component Risk Overview")
            {
                part(ComponentList; "Machine Component Risk Part")
                {
                    ApplicationArea = All;
                    Editable = false;
                }
            }
        }
    }


    actions
    {
        area(Promoted)
        {
            group(Group5)
            {
                ShowAs = SplitButton;
                actionref(MyPromotedActionRef; LogMaintenance)
                {
                }
                actionref(MyThirdPromotedActionRef; CreateMachine)
                {
                }
            }

            group(Group4)
            {
                ShowAs = SplitButton;
                actionref(PromotedActionAddScheduleEntry; AddScheduleEntry)
                {
                }
                actionref(MySecondPromotedActionRef; OpenSchedule)
                {
                }
            }
            group(Group2)
            {
                ShowAs = SplitButton;

                actionref(Group2Btn1; UploadDataset)
                {
                }
                actionref(Group2Btn2; ManageMachines)
                {
                }

                actionref(Group2Btn5; ManageMachineTypes)
                {
                }
                actionref(Group2Btn6; ManageMachineComponents)
                {
                }

                actionref(Group2Btn3; ManageMaintenance)
                {
                }
                actionref(Group2Btn4; ManagePredictedRUL)
                {
                }
            }
            group(Group3)
            {
                ShowAs = SplitButton;

                actionref(Group3ActionRef2; RequestPredictionForAll)
                {
                }
                actionref(Group3ActionRef1; RequestPrediction)
                {
                }
                actionref(Group3ActionRef3; RequestModelTraining)
                {
                }
            }
        }
        area(processing)
        {
            action(LogMaintenance)
            {
                ApplicationArea = All;
                Caption = 'Log Maintenance Event';
                Image = Add;
                trigger OnAction()
                begin
                    PAGE.RUNMODAL(PAGE::"Log Maintenance Event");
                end;
            }

            action(CreateMachine)
            {
                ApplicationArea = All;
                Caption = 'Create Machine';
                Image = Add;
                trigger OnAction()
                begin
                    PAGE.RUNMODAL(PAGE::"Create Machine");
                    CurrPage.Update(true);
                end;
            }

            action(AddScheduleEntry)
            {
                Caption = 'Add Rental/Service';
                ApplicationArea = All;
                Image = Calendar;
                trigger OnAction()
                begin
                    PAGE.RUNMODAL(PAGE::"Add Schedule Entry");
                end;
            }
            action(OpenSchedule)
            {
                Caption = 'Open Schedule';
                ApplicationArea = All;
                Image = Calendar;
                trigger OnAction()
                begin
                    PAGE.RUNMODAL(PAGE::"Machine Schedule Calendar");
                end;
            }

            action(ManageMachines)
            {
                ApplicationArea = All;
                Caption = 'Manage Machines';
                Image = List;
                trigger OnAction()
                begin
                    PAGE.RUNMODAL(PAGE::"Machines");
                end;
            }

            action(ManageMachineTypes)
            {
                ApplicationArea = All;
                Caption = 'Manage Machine Types';
                Image = List;
                trigger OnAction()
                begin
                    PAGE.RUNMODAL(PAGE::"Machine Types");
                end;
            }

            action(ManageMachineComponents)
            {
                ApplicationArea = All;
                Caption = 'Manage Machine Components';
                Image = List;
                trigger OnAction()
                begin
                    PAGE.RUNMODAL(PAGE::"Machine Component");
                end;
            }

            action(ManageMaintenance)
            {
                ApplicationArea = All;
                Caption = 'Manage Maintenance Events';
                Image = List;
                trigger OnAction()
                begin
                    PAGE.RUNMODAL(PAGE::"Maintenance Events");
                end;
            }

            action(ManagePredictedRUL)
            {
                ApplicationArea = All;
                Caption = 'Manage Predictions';
                Image = List;
                trigger OnAction()
                begin
                    PAGE.RUNMODAL(PAGE::"Machine Component Risk");
                end;
            }

            action(UploadDataset)
            {
                Caption = 'Upload Dataset (CSV)';
                ApplicationArea = All;
                Image = Import;

                trigger OnAction()
                var
                    InStream: InStream;
                    FileName: Text;
                    Parser: Codeunit "Simple CSV Parser";
                    Lines: List of [Text[1000]];
                    Line: Text;
                    Fields: array[10] of Text;
                    ParsedList: List of [Text];
                    i: Integer;
                    machineID: Code[20];
                    machineType: Text[50];
                    activeTime: Decimal;
                    faultType: Text[50];
                    repairType: Text[50];
                    cost: Decimal;
                    eventType: Enum "Maintenance Event Type";
                    MachineRec: Record "Machine";
                    EventRec: Record "Maintenance Event";
                    MachineTypeRec: Record "Machine Type";
                    ComponentRec: Record "Machine Component";
                    SkipHeader: Boolean;
                    Dialog: Dialog;
                    Temp: array[10] of Text;
                begin
                    if UploadIntoStream('Select CSV File', '', 'CSV Files (*.csv)|*.csv', FileName, InStream) then begin
                        Dialog.Open('Saving the data. Please wait...');
                        Lines := Parser.LoadFromStream(InStream, ',');

                        foreach Line in Lines do begin
                            if not SkipHeader then begin
                                SkipHeader := true;
                                continue;
                            end;

                            /*
                                Can't assign the output from the parser to the 'Field', like:
                                    Fields := Parser.ParseLine(Line, ',');
                                Which is weird when the ParseLine returns: 
                                    array[10] of Text
                                which is the type of Fields.

                                Instead manually assigning each element in the array works.
                                This has the downside of calling the "ParseLine" for every field.
                            */
                            System.CopyArray(Fields, Parser.ParseLine(Line, ','), 0);
                            /*
                            Fields[1] := Parser.ParseLine(Line, ',') [1];
                            Fields[2] := Parser.ParseLine(Line, ',') [2];
                            Fields[3] := Parser.ParseLine(Line, ',') [3];
                            Fields[4] := Parser.ParseLine(Line, ',') [4];
                            Fields[5] := Parser.ParseLine(Line, ',') [5];
                            Fields[6] := Parser.ParseLine(Line, ',') [6];
                            Fields[7] := Parser.ParseLine(Line, ',') [7];
                            Fields[8] := Parser.ParseLine(Line, ',') [8];
                            Fields[9] := Parser.ParseLine(Line, ',') [9];
                            Fields[10] := Parser.ParseLine(Line, ',') [10];
                            */

                            machineID := Fields[1];
                            machineType := Fields[2];
                            Evaluate(activeTime, Fields[3]);
                            faultType := Fields[4];
                            repairType := Fields[5];
                            Evaluate(cost, Fields[6]);
                            Evaluate(eventType, Fields[7]);

                            // Create not duplicate machine type
                            if not MachineTypeRec.Get(machineType) then begin
                                MachineTypeRec.Init();
                                MachineTypeRec."Machine Type ID" := machineType;
                                MachineTypeRec.Insert();
                            end;

                            // Create not duplicate machine
                            if not MachineRec.Get(machineID) then begin
                                MachineRec.Init();
                                MachineRec."Machine ID" := machineID;
                                MachineRec."Machine Type" := MachineTypeRec."Machine Type ID";
                                MachineRec.Insert();
                            end;

                            // Create no duplicate machine component type
                            if not ComponentRec.Get(faultType) then begin
                                ComponentRec.Init();
                                ComponentRec."Component Name ID" := faultType;
                                ComponentRec.Insert();
                            end;

                            EventRec.Init();
                            if EventRec.FindLast() then
                                EventRec."Entry No." := EventRec."Entry No." + 1
                            else
                                EventRec."Entry No." := 1;
                            EventRec."Machine ID" := machineID;
                            EventRec."Active Time" := activeTime;
                            EventRec."Fault Type" := ComponentRec."Component Name ID";
                            // EventRec."Repair/Replace Type" := repairType;
                            EventRec."Cost" := cost;
                            EventRec."Event Type" := eventType;
                            EventRec.Insert();
                        end;
                        Dialog.Close();

                        Message('CSV data imported successfully.');
                        UpdateMetrics();
                    end;
                end;
            }

            action(RequestPrediction)
            {
                Caption = 'Predict RUL (one)';
                ApplicationArea = All;
                Image = Forecast;

                trigger OnAction()
                var
                    HttpClient: HttpClient;
                    ContentHeaders: HttpHeaders;
                    RequestContent: HttpContent;
                    ResponseMessage: HttpResponseMessage;
                    Content: Text;
                    JsonObject: JsonObject;
                    JsonToken: JsonToken;
                    JsonArray: JsonArray;
                    JsonRequest: JsonObject;
                    JsonComponent: JsonObject;
                    ResultsArray: JsonArray;
                    ResultObj: JsonObject;
                    ComponentName: JsonToken;
                    Component: Text[50];
                    PredictedRULToken: JsonToken;
                    PredictedRUL: Decimal;
                    RiskLevelToken: JsonToken;
                    RiskLevelStr: Text;
                    RiskLevel: Enum "Risk Level";
                    MessageText: Text;
                    MachineIdToken: JsonToken;
                    MachineTypeText: Text[50];
                    MachinesArray: JsonArray;
                    EventsArray: JsonArray;
                    MachineJson: JsonObject;
                    EventJson: JsonObject;
                    JsonText: Text;
                    MachineID: Code[20];
                    MachineRec: Record "Machine";
                    EventRec: Record "Maintenance Event";
                    AssessRec: Record "Machine Component Assessment";
                    Dialog: Dialog;
                begin
                    if PAGE.RunModal(PAGE::"Machines", MachineRec) = ACTION::LookupOK then begin
                        Dialog.Open('Preparing the data. Please wait...');
                        MachineID := MachineRec."Machine ID";
                        JsonRequest.Add('machine_id', MachineID);

                        // Create a json object which contains all of the machines from the table "Machine"
                        if MachineRec.FindSet() then begin
                            repeat
                                Clear(MachineJson);
                                MachineJson.Add('machine_id', MachineRec."Machine ID");
                                MachineJson.Add('machine_type', MachineRec."Machine Type");
                                MachinesArray.Add(MachineJson);
                            until MachineRec.Next() = 0;
                        end;

                        // Create the json object that contains all of the events from the table "Maintenance Event"
                        if EventRec.FindSet() then begin
                            repeat
                                Clear(EventJson);

                                EventJson.Add('machine_id', EventRec."Machine ID");
                                EventJson.Add('active_time', EventRec."Active Time");
                                EventJson.Add('fault_type', EventRec."Fault Type");
                                // EventJson.Add('repair_type', EventRec."Repair/Replace Type");
                                EventJson.Add('cost', EventRec."Cost");
                                EventJson.Add('event_type', Format(EventRec."Event Type"));
                                EventsArray.Add(EventJson);
                            until EventRec.Next() = 0;
                        end;

                        JsonRequest.Add('machines', MachinesArray);
                        JsonRequest.Add('events', EventsArray);
                        JsonRequest.WriteTo(JsonText);

                        RequestContent.WriteFrom(JsonText);
                        RequestContent.GetHeaders(ContentHeaders);
                        ContentHeaders.Clear();
                        ContentHeaders.Add('Content-Type', 'application/json');

                        Dialog.Open('Sending data and running prediction. Please wait...');

                        if HttpClient.Post('http://REDACTED_IP:8000/predict', RequestContent, ResponseMessage) then begin
                            ResponseMessage.Content().ReadAs(Content);
                            if JsonObject.ReadFrom(Content) then begin
                                if JsonObject.Get('predictions', JsonToken) then begin
                                    JsonArray := JsonToken.AsArray();
                                    MessageText := 'Prediction results:\';

                                    foreach JsonToken in JsonArray do begin
                                        JsonToken.AsObject().Get('machine_id', MachineIdToken);
                                        MachineID := MachineIdToken.AsValue().AsText();

                                        if not MachineRec.Get(MachineID) then
                                            continue;

                                        MachineTypeText := MachineRec."Machine Type";

                                        if not JsonToken.AsObject().Get('results', JsonToken) then
                                            continue;

                                        ResultsArray := JsonToken.AsArray();
                                        foreach JsonToken in ResultsArray do begin
                                            ResultObj := JsonToken.AsObject();
                                            JsonComponent := JsonToken.AsObject();

                                            JsonComponent.Get('component', ComponentName);
                                            Component := ComponentName.AsValue().AsText();
                                            JsonComponent.Get('risk_level', RiskLevelToken);
                                            JsonComponent.Get('predicted_rul', PredictedRULToken);
                                            PredictedRUL := PredictedRULToken.AsValue().AsDecimal();
                                            RiskLevelStr := RiskLevelToken.AsValue().AsText();
                                            case RiskLevelStr of
                                                'High Risk':
                                                    RiskLevel := RiskLevel::High;
                                                'Medium Risk':
                                                    RiskLevel := RiskLevel::Medium;
                                                'Low Risk':
                                                    RiskLevel := RiskLevel::Low;
                                                else
                                                    RiskLevel := RiskLevel::Unknown;
                                            end;

                                            MessageText += StrSubstNo('%1 → RUL: %2 minutes, %3\', ComponentName, Round(PredictedRUL, 0.01), RiskLevel);

                                            AssessRec.Reset();
                                            AssessRec.SetRange("Machine ID", MachineID);
                                            AssessRec.SetRange("Component", Component);
                                            if AssessRec.FindFirst() then begin
                                                AssessRec.Validate("Machine Type", MachineTypeText);
                                                AssessRec.Validate("Predicted RUL (mins)", PredictedRUL);
                                                AssessRec.Validate("Risk Level", RiskLevel);
                                                AssessRec.Modify(true);
                                            end else begin
                                                AssessRec.Init();
                                                AssessRec.Validate("Machine ID", MachineID);
                                                AssessRec.Validate("Component", Component);
                                                AssessRec.Validate("Machine Type", MachineTypeText);
                                                AssessRec.Validate("Predicted RUL (mins)", PredictedRUL);
                                                AssessRec.Validate("Risk Level", RiskLevel);
                                                AssessRec."Entry ID" := AssessRec.Count + 1;
                                                AssessRec.Insert(true);
                                            end;
                                        end;

                                        Message(MessageText);
                                    end;
                                end else
                                    Message('No predictions returned.');
                            end else
                                Message('Failed to parse JSON.');
                        end else
                            Message('HTTP request failed.');
                        Dialog.Close();
                    end;
                end;
            }

            action(RequestPredictionForAll)
            {
                Caption = 'Predict RUL (all)';
                ApplicationArea = All;
                Image = Forecast;

                trigger OnAction()
                var
                    HttpClient: HttpClient;
                    ContentHeaders: HttpHeaders;
                    RequestContent: HttpContent;
                    ResponseMessage: HttpResponseMessage;
                    Content: Text;
                    JsonObject: JsonObject;
                    JsonToken: JsonToken;
                    PredictionsArray: JsonArray;
                    MachineObj: JsonObject;
                    ResultsArray: JsonArray;
                    ResultObj: JsonObject;
                    ComponentName: JsonToken;
                    PredictedRULToken: JsonToken;
                    JsonRequest: JsonObject;
                    MachinesArray: JsonArray;
                    EventsArray: JsonArray;
                    MachineJson: JsonObject;
                    EventJson: JsonObject;
                    JsonText: Text;
                    MachineRec: Record "Machine";
                    EventRec: Record "Maintenance Event";
                    AssessRec: Record "Machine Component Assessment";
                    MachineIdToken: JsonToken;
                    MachineID: Code[20];
                    Component: Text[50];
                    PredictedRUL: Decimal;
                    RiskLevelToken: JsonToken;
                    RiskLevelStr: Text;
                    RiskLevel: Enum "Risk Level";
                    MachineTypeText: Text[50];
                    Dialog: Dialog;
                begin
                    Dialog.Open('Preparing the data. Please wait...');

                    // Create a json object which contains all of the machines from the table "Machine"
                    if MachineRec.FindSet() then begin
                        repeat
                            Clear(MachineJson);
                            MachineJson.Add('machine_id', MachineRec."Machine ID");
                            MachineJson.Add('machine_type', MachineRec."Machine Type");
                            MachinesArray.Add(MachineJson);
                        until MachineRec.Next() = 0;
                    end;

                    // Create the json object that contains all of the events from the table "Maintenance Event"
                    if EventRec.FindSet() then begin
                        repeat
                            Clear(EventJson);
                            EventJson.Add('machine_id', EventRec."Machine ID");
                            EventJson.Add('active_time', EventRec."Active Time");
                            EventJson.Add('fault_type', EventRec."Fault Type");
                            // EventJson.Add('repair_type', EventRec."Repair/Replace Type");
                            EventJson.Add('cost', EventRec."Cost");
                            EventJson.Add('event_type', Format(EventRec."Event Type"));
                            EventsArray.Add(EventJson);
                        until EventRec.Next() = 0;
                    end;

                    JsonRequest.Add('machines', MachinesArray);
                    JsonRequest.Add('events', EventsArray);
                    JsonRequest.WriteTo(JsonText);

                    RequestContent.WriteFrom(JsonText);
                    RequestContent.GetHeaders(ContentHeaders);
                    ContentHeaders.Clear();
                    ContentHeaders.Add('Content-Type', 'application/json');

                    Dialog.Open('Sending data and running predictions. Please wait...');

                    if not HttpClient.Post('http://REDACTED_IP:8000/predict-all', RequestContent, ResponseMessage) then begin
                        Message('HTTP request failed.');
                        exit;
                    end;

                    /*
                        The backend returns one array where each element in the array consists of:
                        [
                            "machine_id": integer,
                            "results": [
                                {
                                    "component": string,
                                    "predicted_rul": float,
                                    "risk_level": string (High Risk, Medium Risk, Low Risk)
                                },
                                ...
                            ],
                            ...
                        ]
                    */

                    Dialog.Open('Handling response from server. Please wait...');
                    ResponseMessage.Content().ReadAs(Content);
                    if not JsonObject.ReadFrom(Content) then begin
                        Message('Failed to parse JSON.');
                        exit;
                    end;

                    if not JsonObject.Get('predictions', JsonToken) then begin
                        Message('No predictions returned.');
                        exit;
                    end;

                    PredictionsArray := JsonToken.AsArray();

                    foreach JsonToken in PredictionsArray do begin
                        MachineObj := JsonToken.AsObject();
                        MachineObj.Get('machine_id', MachineIdToken);
                        MachineID := MachineIdToken.AsValue().AsText();

                        if not MachineRec.Get(MachineID) then
                            continue;

                        MachineTypeText := MachineRec."Machine Type";

                        if not MachineObj.Get('results', JsonToken) then
                            continue;

                        ResultsArray := JsonToken.AsArray();
                        foreach JsonToken in ResultsArray do begin
                            ResultObj := JsonToken.AsObject();

                            ResultObj.Get('component', ComponentName);
                            ResultObj.Get('predicted_rul', PredictedRULToken);
                            ResultObj.Get('risk_level', RiskLevelToken);

                            Component := ComponentName.AsValue().AsText();
                            PredictedRUL := PredictedRULToken.AsValue().AsDecimal();
                            RiskLevelStr := RiskLevelToken.AsValue().AsText();

                            case RiskLevelStr of
                                'High Risk':
                                    RiskLevel := RiskLevel::High;
                                'Medium Risk':
                                    RiskLevel := RiskLevel::Medium;
                                'Low Risk':
                                    RiskLevel := RiskLevel::Low;
                                else
                                    RiskLevel := RiskLevel::Unknown;
                            end;

                            // First reset the existing "Machine Component Assessment" table,
                            // Then insert newest prediction
                            AssessRec.Reset();
                            AssessRec.SetRange("Machine ID", MachineID);
                            AssessRec.SetRange("Component", Component);
                            if AssessRec.FindFirst() then begin
                                AssessRec.Validate("Machine Type", MachineTypeText);
                                AssessRec.Validate("Predicted RUL (mins)", PredictedRUL);
                                AssessRec.Validate("Risk Level", RiskLevel);
                                AssessRec.Modify(true);
                            end else begin
                                AssessRec.Init();
                                AssessRec.Validate("Machine ID", MachineID);
                                AssessRec.Validate("Component", Component);
                                AssessRec.Validate("Machine Type", MachineTypeText);
                                AssessRec.Validate("Predicted RUL (mins)", PredictedRUL);
                                AssessRec.Validate("Risk Level", RiskLevel);
                                AssessRec."Entry ID" := 0;
                                AssessRec.Insert(true);
                            end;
                        end;
                    end;
                    Dialog.Close();

                    // Update the page metrics but also use the updated metrics to display the message:
                    UpdateMetrics();
                    //MessageText += StrSubstNo('%1 (%2) → RUL: %3 hrs, Risk: %4\',
                    //    MachineID, Component, Round(PredictedRUL, 0.01), Format(RiskLevel));

                    Message('%1 High Risk components \%2 Medium Risk components',
                            HighRiskCount, MediumRiskCount);
                end;
            }


            action(RequestModelTraining)
            {
                Caption = 'Train Model';
                ApplicationArea = All;
                Image = CalculateWIP;

                trigger OnAction()
                var
                    HttpClient: HttpClient;
                    ContentHeaders: HttpHeaders;
                    RequestContent: HttpContent;
                    ResponseMessage: HttpResponseMessage;
                    JsonRequest: JsonObject;
                    MachinesArray: JsonArray;
                    EventsArray: JsonArray;
                    MachineJson: JsonObject;
                    EventJson: JsonObject;
                    JsonText: Text;
                    MachineRec: Record "Machine";
                    EventRec: Record "Maintenance Event";
                    Dialog: Dialog;
                begin
                    Dialog.Open('Preparing the data. Please wait...');

                    // Create a json object which contains all of the machines from the table "Machine"
                    if MachineRec.FindSet() then begin
                        repeat
                            Clear(MachineJson);
                            MachineJson.Add('machine_id', MachineRec."Machine ID");
                            MachineJson.Add('machine_type', MachineRec."Machine Type");
                            MachinesArray.Add(MachineJson);
                        until MachineRec.Next() = 0;
                    end;

                    // Create the json object that contains all of the events from the table "Maintenance Event"
                    if EventRec.FindSet() then begin
                        repeat
                            Clear(EventJson);

                            EventJson.Add('machine_id', EventRec."Machine ID");
                            EventJson.Add('active_time', EventRec."Active Time");
                            EventJson.Add('fault_type', EventRec."Fault Type");
                            // EventJson.Add('repair_type', EventRec."Repair/Replace Type");
                            EventJson.Add('cost', EventRec."Cost");
                            EventJson.Add('event_type', Format(EventRec."Event Type"));
                            EventsArray.Add(EventJson);
                        until EventRec.Next() = 0;
                    end;

                    JsonRequest.Add('machines', MachinesArray);
                    JsonRequest.Add('events', EventsArray);
                    JsonRequest.WriteTo(JsonText);

                    RequestContent.WriteFrom(JsonText);
                    RequestContent.GetHeaders(ContentHeaders);
                    ContentHeaders.Clear();
                    ContentHeaders.Add('Content-Type', 'application/json');

                    Dialog.Open('Sending the data and training the model. Please wait...');

                    HttpClient.Post('http://REDACTED_IP:8000/train', RequestContent, ResponseMessage);

                    // The backend only returns if the model was successfully trained or not
                    // Success, code: 200, body: {"status": "Model trained"}
                    // Failed,  code: 500, body: the error

                    if ResponseMessage.HttpStatusCode = 200 then begin
                        Message('Model trained successfully');
                    end else begin
                        Message('Error in training model, verify the data and try again');
                    end;
                    Dialog.Close();
                end;
            }
        }
    }
    protected var
        HighRiskCount: Integer;
        MediumRiskCount: Integer;

    var
        TotalMachines: Integer;
        TotalEvents: Integer;
        LastPredictionDate: DateTime;

    procedure UpdateMetrics()
    var
        MachineRec: Record Machine;
        MachineEventsRec: Record "Maintenance Event";
        AssessRec: Record "Machine Component Assessment";
    begin
        TotalMachines := MachineRec.Count;
        TotalEvents := MachineEventsRec.Count;

        // Count high risk and medium risk components
        HighRiskCount := 0;
        AssessRec.SetRange("Risk Level", AssessRec."Risk Level"::High);
        if AssessRec.FindSet() then
            repeat
                HighRiskCount += 1;
            until AssessRec.Next() = 0;

        MediumRiskCount := 0;
        AssessRec.SetRange("Risk Level", AssessRec."Risk Level"::Medium);
        if AssessRec.FindSet() then
            repeat
                MediumRiskCount += 1;
            until AssessRec.Next() = 0;

        // Find the oldest assessment date
        LastPredictionDate := CreateDateTime(DMY2Date(31, 12, 9999), Time());
        if AssessRec.FindSet() then
            repeat
                if AssessRec."Assessment Date" < LastPredictionDate then
                    LastPredictionDate := AssessRec."Assessment Date";
            until AssessRec.Next() = 0;
    end;

    trigger OnOpenPage();
    begin
        UpdateMetrics();
    end;
}
