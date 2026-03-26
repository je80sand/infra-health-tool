def generate_ai_analysis(report_data):
    target = report_data.get("target", "unknown target")
    sent = report_data.get("packets_sent", 0)
    received = report_data.get("packets_received", 0)
    loss = report_data.get("packet_loss_percent", 0)
    latency = report_data.get("average_latency_ms")

    if sent > 0:
        success_rate = (received / sent) * 100
    else:
        success_rate = 0

    if success_rate >= 99:
        status = "excellent"
    elif success_rate >= 95:
        status = "good"
    elif success_rate >= 85:
        status = "unstable"
    else:
        status = "critical"

    findings = [
        f"Connectivity to {target} is {status} with a {success_rate:.1f}% success rate."
    ]

    if loss == 0:
        findings.append("No packet loss was detected.")
    elif loss <= 5:
        findings.append(f"Minor packet loss was detected at {loss}%.")
    elif loss <= 15:
        findings.append(f"Moderate packet loss was detected at {loss}%.")
    else:
        findings.append(f"Severe packet loss was detected at {loss}%.")

    if latency is None:
        findings.append("Average latency was not available.")
    elif latency < 50:
        findings.append(f"Average latency is healthy at {latency} ms.")
    elif latency < 100:
        findings.append(f"Average latency is a little high at {latency} ms.")
    else:
        findings.append(f"Average latency is high at {latency} ms.")

    causes = []
    if loss > 0:
        causes.append("Wi-Fi signal issues or interference")
        causes.append("ISP instability")
        causes.append("Router or modem problems")

    if latency is not None and latency >= 100:
        causes.append("Network congestion")
        causes.append("Routing issues")

    if not causes:
        causes.append("No major issues were detected")

    recommendations = []
    if loss > 0:
        recommendations.append("Run the test again at different times")
        recommendations.append("Compare Wi-Fi and Ethernet results")
        recommendations.append("Reboot your router and retest")

    if latency is not None and latency >= 100:
        recommendations.append("Test another target to compare latency")
        recommendations.append("Avoid heavy internet use during testing")

    if not recommendations:
        recommendations.append("No immediate action is needed")
        recommendations.append("Use this report as a healthy baseline")

    return {
        "summary": findings[0],
        "findings": findings,
        "possible_causes": causes,
        "recommendations": recommendations,
    }