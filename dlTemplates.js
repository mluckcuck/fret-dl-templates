// dlTempaltes
// Matt Luckcuck, University of Nottingham
// 2024

const fretTemplatesPath = "./"
const ed = require(fretTemplatesPath + 'templateEditor')

function makeTemplates() {

let dlTemplates = []
//============================= No Change (was R2/threshold2)

ed.newTemplate("template-rl-noChange", "RL No Change");
ed.templateSummary("whenever the sample time is not reached (cRL < tS) the RL agent does not change the action");
ed.templateStructure("whenever ([clockTime] < [sampleTime]) RLAgent shall immediately satisfy maintain([varList])");

ed.fieldDescription("clockTime", "The clock's time.");
ed.addOption("clockTime", "cRL", "Replace with clock variable name.");

ed.fieldDescription("sampleTime", "The sample time.");
ed.addOption("sampleTime", "sampleTime",  "Replace with sample time variable name.");

ed.fieldDescription("varList", "The variable to be maintained,");
ed.addOption("varList", "var", "Replace with variable name.")
ed.addOption("varList", "var1, var2,...", "Replace with list of variable names.")

ed.addExample("[cRL][tS][temp]");
ed.addExample("[clockTime][sampleTime][speed]")

dlTemplates.push(ed.createFinalTemplateObject())

// =========================== Choose Action (was R1/threshold2)
ed.newTemplate("template-rl-chooseAction", "RL Choose Action");
ed.templateSummary("Whenever the sample time is reached (cRL >= tS) \
	the RL agent chooses and action that ensures that the worst case reaction of the overall system, \
	within one sample time still maintains the safety threshold.");

ed.templateStructure("whenever ([clockTime] >= [sampleTime]) RLAgent shall immediately satisfy choose([varList])");

ed.fieldDescription("clockTime", "The clock's time.");
ed.addOption("clockTime", "cRL", "Replace with clock variable name.");

ed.fieldDescription("sampleTime", "The sample time.");
ed.addOption("sampleTime", "sampleTime",  "Replace with sample time variable name.");

ed.fieldDescription("varList", "The variable to be maintained,");
ed.addOption("varList", "var", "Replace with variable name.")
ed.addOption("varList", "var1, var2,...", "Replace with list of variable names.")



ed.addExample("[cRL][tS][temp]");
ed.addExample("[clockTime][sampleTime][speed]")

dlTemplates.push(ed.createFinalTemplateObject());

// =========================== System Threshold (was R3/threshold3)

ed.newTemplate("template-rl-systemThreshold", "System Threshold");
ed.templateSummary("Under a given precondition, the system should always satisfy the given threshold.");

ed.templateStructure("if [precondition] System shall always satisfy [threshold]");

ed.fieldDescription("precondition", "Precondition for the threshold.");
ed.addOption("precondition", "precondition", "Replace with the precondition.");

ed.fieldDescription("threshold", "var ~ threshold");
ed.addOption("threshold", "var < threshold", "var less than threshold.");
ed.addOption("threshold", "var <= threshold", "var less than or equal to threshold.");

ed.addExample("[T <= TMAX] [T <= TMAX]");
dlTemplates.push(ed.createFinalTemplateObject());

// =========================== Contract Threshold (also was R1/threshold1)

ed.newTemplate("template-rl-contractThreshold", "Hybrid Contract Threshold");
ed.templateSummary("Whenever the sample time is reached (cRL >= tS), if the safety critical variable [var] is already within the threshold it should, \
	remain within the threshold, event under the [worst case reaction].");
ed.templateStructure("whenever ([clockTime] >= [sampleTime]) RLAgent shall immediately satisfy ([threshold]) => ([var] + [worst case reaction] [thresholdComparison])");


ed.fieldDescription("clockTime", "The clock's time.");
ed.addOption("clockTime", "cRL", "Replace with clock variable name.");

ed.fieldDescription("sampleTime", "The sample time.");
ed.addOption("sampleTime", "sampleTime",  "Replace with sample time variable name.");

ed.fieldDescription("var", "The controlled variable.")
ed.addOption("var", "controlledVariable", "replace with the controlled variable.")


ed.fieldDescription("threshold", "var ~ threshold");
ed.addOption("threshold", "var < threshold", "var less than threshold");
ed.addOption("threshold", "var <= threshold", "var less than or equal to threshold");
ed.addOption("threshold", "var > threshold", "var greater than threshold");
ed.addOption("threshold", "var >= threshold", "var greater than or equal to threshold");

ed.fieldDescription("thresholdComparison","Comparison to the threshold variable.")
ed.addOption("thresholdComparison", "< threshold", "less than threshold");
ed.addOption("thresholdComparison", "<= threshold", "less than or equal to threshold");
ed.addOption("thresholdComparison", "> threshold", "greater than threshold");
ed.addOption("thresholdComparison", ">= threshold", "greater than or equal to threshold");


ed.fieldDescription("worst case reaction", "The worst-case reaction function. Usually this is defined as the realtion between the state, and action, and the recovery time.");
ed.addOption("worst case reaction", "(state - action) * sampleTime", "Usual worst case reaction relationship.");
ed.addOption("worst case reaction", "wcreaction", "Replace with worst-case reaction function.  Usually this is defined as the realtion between the state, and action, and the recovery time.");

ed.addExample("whenever ([cRL] >= [tS]) RLAgent shall immediately satisfy ([T <= TMAX]) => ([T]+[(hMax-c)*ts] [<= TMAX])");


dlTemplates.push(ed.createFinalTemplateObject());


// =========================== System Recovery (new)

ed.newTemplate("template-rl-systemRecovery", "System Recovery");
ed.templateSummary("After some disruption, the system should recover the threshold within the maxRecoveryTime. ");

ed.templateStructure("if [precondition] System shall always satisfy [time since disruption] > [maxRecoveryTime] => [threshold]");

ed.fieldDescription("precondition", "Precondition for the threshold.");
ed.addOption("precondition", "precondition", "Replace with the precondition.");

ed.fieldDescription("time since disruption", "t");
ed.addOption("time since disruption", "t", "Replace with variable representing the time since the disruption.")

ed.fieldDescription("maxRecoveryTime", "maxT");
ed.addOption("maxRecoveryTime", "maxT", "Replace with variable representing the maxRecoveryTime.")

ed.fieldDescription("threshold", "var ~ threshold");
ed.addOption("threshold", "var < threshold", "var less than threshold");
ed.addOption("threshold", "var <= threshold", "var less than or equal to threshold");
ed.addOption("threshold", "var > threshold", "var greater than threshold");
ed.addOption("threshold", "var >= threshold", "var greater than or equal to threshold");

ed.addExample("[T <= TMAX][10][recoveryMax][T <= TMAX]");
dlTemplates.push(ed.createFinalTemplateObject());

//=============================== Contract Recovery (was R4/recovery1)

ed.newTemplate("template-rl-contractRecovery1", "Hybrid Contract Recovery 1")
ed.templateSummary("If the threshold is violated (![threshold]), the RL agent recovers the variable to within safe limits under the worst-case reaction within the recovery time, which can be specified in [worst case recovery]");
ed.templateStructure("whenever ([clockTime] >= [sampleTime]) RLAgent shall immediately satisfy & (![threshold]) => ([var] + [worst case recovery] [thresholdComparison])");

ed.fieldDescription("clockTime", "The clock's time.");
ed.addOption("clockTime", "cRL", "Replace with clock variable name.");

ed.fieldDescription("sampleTime", "The sample time.");
ed.addOption("sampleTime", "sampleTime",  "Replace with sample time variable name.");

ed.fieldDescription("var", "The controlled variable.");
ed.addOption("var", "controlledVariable", "replace with the controlled variable.");

ed.fieldDescription("threshold", "var ~ Threshold");
ed.addOption("threshold", "var < threshold", "var less than threshold");
ed.addOption("threshold", "var <= threshold", "var less than or equal to threshold");
ed.addOption("threshold", "var > threshold", "var greater than threshold");
ed.addOption("threshold", "var >= threshold", "var greater than or equal to threshold");

ed.fieldDescription("thresholdComparison","Comparison to the threshold variable.");
ed.addOption("thresholdComparison", "< threshold", "less than threshold");
ed.addOption("thresholdComparison", "<= threshold", "less than or equal to threshold");
ed.addOption("thresholdComparison", "> threshold", "greater than threshold");
ed.addOption("thresholdComparison", ">= threshold", "greater than or equal to threshold");

ed.fieldDescription("worst case reaction", "The worst-case reaction function. Usually this is defined as the realtion between the state, and action, and the recovery time.");
ed.addOption("worst case reaction", "(state - action) * sampleTime", "Usual worst case reaction relationship.");
ed.addOption("worst case reaction", "wcreaction", "Replace with worst-case reaction function.  Usually this is defined as the realtion between the state, and action, and the recovery time.");

ed.addExample("whenever ([cRL] >= [tS]) RLAgent shall immediately satisfy (![temp > TMAX]) => ([temp] + [worstCoolingtemp] [<= TMAX]).");
//ed.addExample("whenever ([cRL] >= [tS]) RLAgent shall immediately satisfy (![temp > TMAX]) => ([hMax - c*((tDLast+tRMax) - temp]) [<= TMAX]).");

dlTemplates.push(ed.createFinalTemplateObject())



// =============================== Contract Recovery 2 (was R5/recovery2)

ed.newTemplate("template-rl-contractRecovery2", "Hybrid Contract Recovery 2");
ed.templateSummary("If the variable has not been violated, the safety critical variable remains within the threshold.");
ed.templateStructure("whenever ([clockTime] >= [sampleTime]) RLAgent shall immediately satisfy ([threshold]) => ([var] + [worst case reaction] [thresholdComparison])");


ed.fieldDescription("clockTime", "The clock's time.");
ed.addOption("clockTime", "cRL", "Replace with clock variable name.");

ed.fieldDescription("sampleTime", "The sample time.");
ed.addOption("sampleTime", "sampleTime",  "Replace with sample time variable name.");

ed.fieldDescription("var", "The controlled variable.");
ed.addOption("var", "controlledVariable", "replace with the controlled variable.");

ed.fieldDescription("threshold", "var ~ Threshold");
ed.addOption("threshold", "var < threshold", "var less than threshold");
ed.addOption("threshold", "var <= threshold", "var less than or equal to threshold");
ed.addOption("threshold", "var > threshold", "var greater than threshold");
ed.addOption("threshold", "var >= threshold", "var greater than or equal to threshold");

ed.fieldDescription("thresholdComparison","Comparison to the threshold variable.")
ed.addOption("thresholdComparison", "< threshold", "less than threshold");
ed.addOption("thresholdComparison", "<= threshold", "less than or equal to threshold");
ed.addOption("thresholdComparison", "> threshold", "greater than threshold");
ed.addOption("thresholdComparison", ">= threshold", "greater than or equal to threshold");

ed.fieldDescription("worst case reaction", "The worst-case reaction function. Usually this is defined as the realtion between the state, and action, and the recovery time.");
ed.addOption("worst case reaction", "(state - action) * sampleTime", "Usual worst case reaction relationship.");
ed.addOption("worst case reaction", "wcreaction", "Replace with worst-case reaction function.  Usually this is defined as the realtion between the state, and action, and the recovery time.");

ed.addExample("whenever ([cRL >= tS]) RLAgent shall immediately satisfy ([t <= TMAX]) => [t] + [(hMax - c) *tS)] [<= TMAX]");


dlTemplates.push(ed.createFinalTemplateObject());


// =========================== System Resilience (new)

ed.newTemplate("template-rl-systemResilience", "System Resilience");
ed.templateSummary("The system, should provide a degraded service, while maintaining the threshold. ");

ed.templateStructure("if [precondition] System shall always satisfy [threshold] & [action] >= [degradedService]");

ed.fieldDescription("precondition", "Precondition for the threshold.");
ed.addOption("precondition", "precondition", "Replace with the precondition.");

ed.fieldDescription("threshold", "var ~ threshold");
ed.addOption("threshold", "var < threshold", "var less than threshold");
ed.addOption("threshold", "var <= threshold", "var less than or equal to threshold");
ed.addOption("threshold", "var > threshold", "var greater than threshold");
ed.addOption("threshold", "var >= threshold", "var greater than or equal to threshold");

ed.fieldDescription("action", "The action for the worst-case reaction function")
ed.addOption("action", "worstCaseAction","Replace with the action for the worst-case reaction function")

ed.fieldDescription("degradedService", "degradedService");
ed.addOption("degradedService", "degradedService", "Replace with variable representing the degraded service.")

ed.addExample("[T <= TMAX] [T <= TMAX] [action] [degradedService]");
dlTemplates.push(ed.createFinalTemplateObject());

// =============================== Contract Resilience (was R6/resilience1)

ed.newTemplate("template-rl-resilience1", "Hybrid Contract Resilience 1")
ed.templateSummary("If the safety critical variable is more than a sufficient margin ([Delta suff]) within the threshold, facilitating a higher service level action, then an [action] greater or equal to [degradedService] may be selected, ensuring the threshold’s maintenance even under the worst-case reaction.");
ed.templateStructure("whenever ([clockTime] >= [sampleTime]) RLAgent shall immediately \
	satisfy ([threshold] + [deltaSuff]) => [action] >= [degradedService] & ([var] + [worst case reaction] [thresholdComparison])")

ed.fieldDescription("clockTime", "The clock's time.");
ed.addOption("clockTime", "cRL", "Replace with clock variable name.");

ed.fieldDescription("sampleTime", "The sample time.");
ed.addOption("sampleTime", "sampleTime",  "Replace with sample time variable name.");


ed.fieldDescription("var", "The controlled variable.")
ed.addOption("var", "controlledVariable", "replace with the controlled variable.")

ed.fieldDescription("worst case reaction", "The worst-case reaction function. Usually this is defined as the realtion between the state, and action, and the recovery time.")
ed.addOption("worst case reaction", "(state - action) * sampleTime", "Usual worst case reaction relationship.")
ed.addOption("worst case reaction", "wcreaction", "Replace with worst-case reaction function.  Usually this is defined as the realtion between the state, and action, and the recovery time.")

ed.fieldDescription("threshold", "var ~ Threshold");
ed.addOption("threshold", "var < threshold", "var less than threshold");
ed.addOption("threshold", "var <= threshold", "var less than or equal to threshold");
ed.addOption("threshold", "var > threshold", "var greater than threshold");
ed.addOption("threshold", "var >= threshold", "var greater than or equal to threshold");

ed.fieldDescription("action", "The action for the worst-case reaction function")
ed.addOption("action", "worstCaseAction","Replace with the action for the worst-case reaction function")

ed.fieldDescription("deltaSuff" , "A buffer to ensure a higher service level can be provided and a minimum safety level can be maintained.")
ed.addOption("deltaSuff", "deltaSuff", "Replace")

ed.fieldDescription("degradedService", "degradedService");
ed.addOption("degradedService", "degradedService", "Replace with variable representing the degraded service.")

ed.fieldDescription("thresholdComparison","Comparison to the threshold variable.")
ed.addOption("thresholdComparison", "< threshold", "less than threshold");
ed.addOption("thresholdComparison", "<= threshold", "less than or equal to threshold");
ed.addOption("thresholdComparison", "> threshold", "greater than threshold");
ed.addOption("thresholdComparison", ">= threshold", "greater than or equal to threshold");

ed.addExample("whenever ([cRL] >= [tS])  RLAgent shall immediately satisfy ([l] >  [lMin+deltaSuff]) => [s] >= [sDeg] & ([l]+[0*r-s)*(tS)] > [lMin]");

dlTemplates.push(ed.createFinalTemplateObject())




// =============================== Contract Resiliance 2 (was R7/resiliance2)

ed.newTemplate("template-rl-contractResilience2", "Hybrid Contract Resilience 2");
ed.templateSummary("If the safety critical variable is not a sufficient margin ([Delta suff]) within the threshold, then the RL agent defaults to a degraded service action ([action]=[degradedService]).");
ed.templateStructure("whenever ([clockTime] >= [sampleTime]) RLAgent shall immediately satisfy (![threshold] + [deltaSuff]) => [action] = [degradedService]");

ed.fieldDescription("clockTime", "The clock's time.");
ed.addOption("clockTime", "cRL", "Replace with clock variable name.");

ed.fieldDescription("sampleTime", "The sample time.");
ed.addOption("sampleTime", "sampleTime",  "Replace with sample time variable name.");


ed.fieldDescription("threshold", "var ~ Threshold");
ed.addOption("threshold", "var < threshold", "var less than threshold");
ed.addOption("threshold", "var <= threshold", "var less than or equal to threshold");
ed.addOption("threshold", "var > threshold", "var greater than threshold");
ed.addOption("threshold", "var >= threshold", "var greater than or equal to threshold");

ed.fieldDescription("threshold","The controlled variable's threshold.");
ed.addOption("threshold", "variableThreshold", "Replace with the controlled variable's threshold.");


ed.fieldDescription("deltaSuff" , "A buffer to ensure a higher service level can be provided and a minimum safety level can be maintained.");
ed.addOption("deltaSuff", "deltaSuff", "Replace");


ed.fieldDescription("action", "The action for the worst-case reaction function");
ed.addOption("action", "worstCaseAction","Replace with action");

ed.fieldDescription("degradedService", "degradedService");
ed.addOption("degradedService", "degradedService", "Replace with variable representing the degraded service.");



ed.addExample("whenever ([cRL] >= [tS]) RLAgent shall immediately satisfy !([l] > [lMin+deltaSuff]) => [s] = [sDeg]");


dlTemplates.push(ed.createFinalTemplateObject())


return dlTemplates
}

module.exports = {
 makeTemplates
}
