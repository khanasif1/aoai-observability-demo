# ai-demo-world
azure ai demo world


- APIM Auth Config - https://github.com/HoussemDellai/ai-course/blob/main/300_apim_genai_openai/policy.xml
<!-- https://www.youtube.com/watch?v=8u75pIIObpo&t=1037s -->
```
<authentication-managed-identity resource="https://cognitiveservices.azure.com"
            output-token-variable-name="managed-id-access-token" ignore-error="false" />
        <set-header name="Authorization" exists-action="override">
            <value>@("Bearer " + (string)context.Variables["managed-id-access-token"])</value>
        </set-header>

```