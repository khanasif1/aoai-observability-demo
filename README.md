# Azure Open AI - Observability

<p align="center">
  <img  src="https://github.com/khanasif1/ai-demo-world/blob/main/observability/resources/apim.gif">
</p>

## Solution Overview

This repository contains a solution to track per-user consumption and billing for Azure OpenAI services. It integrates:

- Azure APIM for routing and user authentication
- Azure Functions for usage processing and reporting
- OpenTelemetry for observability and logging
- Streamlit for data visualization and billing report display

### Azure Functions

1. azFn-AoAiModel-Pricing

    - Extracts data from Azure open AI pricing page
    - Select price for specific model and version 
    - Return as json the price of selcted model and version

2. azFn-AppInsightAPI

    - Retrieves stored usage and cost data from Application Insights.
    - Provides a REST-style interface to share data with external dashboards or clients.

### OpenTelemetry Console App

- Uses Python OpenTelemetry libraries to trace, measure, and log usage details.
- Links requests from Azure APIM and Azure Functions, providing a full picture of user session data.
- Enables you to isolate specific users through correlated traces for cost assessment.

### Streamlit UI

- Presents a dashboard with both real-time and historical usage costs per user.
- Integrates with the azFn-AppInsightAPI to fetch cost and usage data on demand.
- Lets you sort and filter results, making it straightforward to view costs in detail.

### Architecture Diagram

<p align="center">
  <img  src="https://github.com/khanasif1/ai-demo-world/blob/main/observability/resources/architecture.png">
</p>

### How It Works

1. API requests flow through Azure APIM, leveraging managed identities for secure access.
2. azFn-AoAiModel-Pricing processes and logs usage data from Azure OpenAI models.
3. azFn-AppInsightAPI exposes the cost data from Application Insights as a consumable API.
4. OpenTelemetry Console App monitors and sends structured logs to enhance visibility.
5. Streamlit UI consumes the data to display user-specific cost analytics in a user-friendly dashboard.

Deploy this solution according to Azure Best Practices to maintain optimal security, reliability, and cost management.

- APIM Auth Config - https://github.com/HoussemDellai/ai-course/blob/main/300_apim_genai_openai/policy.xml
<!-- https://www.youtube.com/watch?v=8u75pIIObpo&t=1037s -->
```
<authentication-managed-identity resource="https://cognitiveservices.azure.com"
            output-token-variable-name="managed-id-access-token" ignore-error="false" />
        <set-header name="Authorization" exists-action="override">
            <value>@("Bearer " + (string)context.Variables["managed-id-access-token"])</value>
        </set-header>

```
