pageextension 50103 RiskComponent extends "Predictive Maintenance Hub"
{
    layout
    {
        addafter("Dashboard Overview")
        {
            group("Component Risk Warnings")
            {
                Caption = 'Critical & Advisory Alerts';
                Visible = (HighRiskCount > 0) or (MediumRiskCount > 0);

                field("Immediate Maintenance Required"; HighRiskCount)
                {
                    ApplicationArea = All;
                    Style = Strong;
                    StyleExpr = true;
                    Editable = false;
                    ToolTip = 'These components are in High Risk and need immediate replacement.';
                }

                field("Plan Upcoming Replacement"; MediumRiskCount)
                {
                    ApplicationArea = All;
                    Style = Strong;
                    StyleExpr = true;
                    Editable = false;
                    ToolTip = 'These components are at Medium Risk and should be scheduled soon.';
                }
            }
        }
    }

    actions
    {
        addafter(Group4)
        {
            group(Group6)
            {
                ShowAs = SplitButton;
                actionref(PromotedViewHighRiskPopup; ViewHighRiskPopup)
                {
                }
                actionref(PromotedViewMediumRiskPopup; ViewMediumRiskPopup)
                {
                }
            }
        }
        addafter(RequestModelTraining)
        {
            group(RiskActions)
            {
                Caption = 'Component Risk Review';

                action(ViewHighRiskPopup)
                {
                    Caption = 'View High Risk Components';
                    ApplicationArea = All;
                    Image = Warning;
                    trigger OnAction()
                    var
                        RiskPopupPage: Page "Risk Component Popup";
                        RiskLevel: enum "Risk Level";
                    begin
                        RiskPopupPage.SetRiskFilterLevel(RiskLevel::High);
                        RiskPopupPage.RunModal();
                    end;
                }

                action(ViewMediumRiskPopup)
                {
                    Caption = 'View Medium Risk Components';
                    ApplicationArea = All;
                    Image = Warning;
                    trigger OnAction()
                    var
                        RiskPopupPage: Page "Risk Component Popup";
                        RiskLevel: enum "Risk Level";
                    begin
                        RiskPopupPage.SetRiskFilterLevel(RiskLevel::Medium);
                        RiskPopupPage.RunModal();
                    end;
                }
            }
        }
    }
}
