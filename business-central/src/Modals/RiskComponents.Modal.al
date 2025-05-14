page 50133 "Risk Component Popup"
{
    PageType = List;
    SourceTable = "Machine Component Assessment";
    ApplicationArea = All;
    Caption = 'Component Risk Overview';
    UsageCategory = None;
    Editable = false;

    layout
    {
        area(content)
        {
            repeater(CompList)
            {
                field("Machine ID"; Rec."Machine ID") { ApplicationArea = All; }
                field(Component; Rec.Component) { ApplicationArea = All; }
                field("Predicted RUL"; Rec."Predicted RUL (mins)") { ApplicationArea = All; }
                field("Risk Level"; Rec."Risk Level") { ApplicationArea = All; }
            }
        }
    }

    actions
    {
        area(Promoted)
        {
            actionref(PromotedActionHighRiskFilter; HighRiskFilter)
            {
            }
            actionref(PromotedActionMediumRiskFilter; MediumRiskFilter)
            {
            }
            actionref(PromotedActionScheduleMaintenance; ScheduleMaintenance)
            {
            }
        }
        area(processing)
        {
            action(HighRiskFilter)
            {
                Caption = 'Filter High Risk';
                ApplicationArea = All;
                Image = Filter;
                Enabled = (RiskFilterToggle = Rec."Risk Level"::Medium);
                trigger OnAction()
                begin
                    SetRiskFilterLevel(Rec."Risk Level"::High);
                    CurrPage.Update(false);
                end;
            }
            action(MediumRiskFilter)
            {
                Caption = 'Filter Medium Risk';
                ApplicationArea = All;
                Image = Filter;
                Enabled = (RiskFilterToggle = Rec."Risk Level"::High);
                trigger OnAction()
                begin
                    SetRiskFilterLevel(Rec."Risk Level"::Medium);
                    CurrPage.Update(false);
                end;
            }

            action(ScheduleMaintenance)
            {
                Caption = 'Schedule Maintenance';
                ApplicationArea = All;
                Image = Calendar;
                Enabled = ((Rec."Risk Level" = Rec."Risk Level"::High) or (Rec."Risk Level" = Rec."Risk Level"::Medium));

                trigger OnAction()
                var
                    SelectedRec: Record "Machine Component Assessment";
                    SchedRec: Record "Machine Schedule";
                    ScheduleDialog: Page "Schedule Input Dialog";
                    MachineRec: Record Machine;
                    StartDT: DateTime;
                    EndDT: DateTime;
                begin
                    CurrPage.SetSelectionFilter(SelectedRec);

                    if SelectedRec.FindSet() then begin
                        if ScheduleDialog.RunModal() = Action::OK then begin
                            StartDT := ScheduleDialog.GetStart();
                            EndDT := ScheduleDialog.GetEnd();

                            SchedRec.Init();
                            SchedRec."Schedule ID" := (SchedRec.Count + 1).ToText();
                            MachineRec.Get(SelectedRec."Machine ID");
                            SchedRec."Machine ID" := MachineRec."Machine ID";
                            SchedRec.Component := SelectedRec.Component;
                            SchedRec."Start Date" := StartDT;
                            SchedRec."End Date" := EndDT;
                            SchedRec."Event Type" := SchedRec."Event Type"::PreemptiveReplacement;
                            SchedRec.Insert(true);

                            Message(
                                'Maintenance scheduled for Machine: %1, Component: %2 \From %3 to %4',
                                SelectedRec."Machine ID",
                                SelectedRec.Component,
                                StartDT,
                                EndDT
                            );
                        end;
                    end;
                end;
            }
        }
    }

    var
        RiskFilterToggle: enum "Risk Level";

    procedure SetRiskFilterLevel(Level: enum "Risk Level")
    begin
        RiskFilterToggle := Level;
        ApplyRiskFilter();
    end;

    procedure ApplyRiskFilter()
    begin
        case RiskFilterToggle of
            RiskFilterToggle::High:
                Rec.SetRange("Risk Level", Rec."Risk Level"::High);
            RiskFilterToggle::Medium:
                Rec.SetRange("Risk Level", Rec."Risk Level"::Medium);
            RiskFilterToggle::Unknown:
                Rec.SetRange("Risk Level");
        end;
    end;

    trigger OnOpenPage()
    begin
        ApplyRiskFilter();
    end;

    trigger OnAfterGetCurrRecord()
    begin
        ApplyRiskFilter();
    end;
}
