/**
 * PromptKiller — Platform Knowledge Base
 * Security profiles for specific platforms, services, and technologies
 * Used by the Strategy Generator to create platform-specific strategies
 */

const PLATFORMS = {
    // ═══════════════════════════════════════════════
    // CLOUD PROVIDERS
    // ═══════════════════════════════════════════════
    aws: {
        name: "Amazon Web Services (AWS)",
        icon: "☁️",
        category: "cloud",
        vulnerabilities: [
            "IAM misconfiguration (overprivileged roles)",
            "S3 bucket public exposure",
            "Lambda function injection",
            "EC2 metadata service SSRF",
            "CloudTrail log tampering",
            "Secrets Manager leaks",
            "VPC peering misconfig",
            "RDS public endpoints"
        ],
        owasp_mapping: ["A01:2021-Broken Access Control", "A05:2021-Security Misconfiguration"],
        cwe: ["CWE-284", "CWE-532", "CWE-668"],
        tools: ["Prowler", "ScoutSuite", "CloudSploit", "pacu", "enumerate-iam"],
        detection_patterns: [
            "aws iam get-account-authorization-details",
            "aws s3api list-buckets --query 'Buckets[].Name'",
            "aws lambda list-functions",
            "aws ec2 describe-instances"
        ],
        secure_coding: [
            "Use IAM roles instead of access keys",
            "Enable S3 bucket policies with explicit deny",
            "Use AWS Secrets Manager for credentials",
            "Enable CloudTrail in all regions",
            "Use VPC endpoints for AWS services"
        ],
        remediation: [
            "Apply least-privilege IAM policies",
            "Enable MFA on all root and IAM users",
            "Restrict S3 bucket public access",
            "Enable GuardDuty for threat detection",
            "Use AWS Config for compliance monitoring"
        ]
    },

    azure: {
        name: "Microsoft Azure",
        icon: "🔷",
        category: "cloud",
        vulnerabilities: [
            "Azure AD misconfiguration",
            "Blob storage public access",
            "Azure Functions injection",
            "Managed Identity abuse",
            "Key Vault access policy bypass",
            "NSG rule misconfiguration",
            "Azure DevOps pipeline injection",
            "Cosmos DB SQL injection"
        ],
        owasp_mapping: ["A01:2021-Broken Access Control", "A05:2021-Security Misconfiguration"],
        cwe: ["CWE-284", "CWE-532", "CWE-918"],
        tools: ["ROADtools", "MicroBurst", "AzureHound", "Stormspotter", "AADInternals"],
        detection_patterns: [
            "az ad sp list --all",
            "az storage account list",
            "az functionapp list",
            "az keyvault list"
        ],
        secure_coding: [
            "Use Managed Identities instead of service principals",
            "Enable Azure AD Conditional Access",
            "Use Azure Key Vault for secrets",
            "Enable Azure Security Center",
            "Use Private Endpoints for PaaS services"
        ],
        remediation: [
            "Review Azure AD permissions regularly",
            "Enable MFA for all users",
            "Restrict blob storage public access",
            "Enable Microsoft Defender for Cloud",
            "Use Azure Policy for compliance"
        ]
    },

    gcp: {
        name: "Google Cloud Platform (GCP)",
        icon: "🔶",
        category: "cloud",
        vulnerabilities: [
            "GCP IAM misconfiguration",
            "Cloud Storage bucket exposure",
            "Cloud Functions injection",
            "Service account key exposure",
            "GKE cluster misconfiguration",
            "BigQuery data exfiltration",
            "Firestore injection",
            "Cloud Run privilege escalation"
        ],
        owasp_mapping: ["A01:2021-Broken Access Control", "A05:2021-Security Misconfiguration"],
        cwe: ["CWE-284", "CWE-532", "CWE-668"],
        tools: ["ScoutSuite", "GCPBucketBrute", "red_snapshot", "Platypus", "gcp-iam-escalator"],
        detection_patterns: [
            "gcloud projects list",
            "gcloud iam service-accounts list",
            "gsutil ls",
            "gcloud functions list"
        ],
        secure_coding: [
            "Use workload identity instead of service account keys",
            "Enable VPC Service Controls",
            "Use Secret Manager for credentials",
            "Enable Cloud Audit Logs",
            "Use Organization Policy constraints"
        ],
        remediation: [
            "Review IAM bindings regularly",
            "Enable MFA for all users",
            "Restrict public bucket access",
            "Enable Security Command Center",
            "Use Binary Authorization for GKE"
        ]
    },

    // ═══════════════════════════════════════════════
    // WEB FRAMEWORKS
    // ═══════════════════════════════════════════════
    react: {
        name: "React / Next.js",
        icon: "⚛️",
        category: "web_framework",
        vulnerabilities: [
            "XSS via dangerouslySetInnerHTML",
            "Server-Side Rendering (SSR) injection",
            "Client-side routing bypass",
            "React hydration mismatch exploitation",
            "API route authentication bypass",
            "Server Actions injection",
            "Middleware bypass",
            "Cache poisoning"
        ],
        owasp_mapping: ["A03:2021-Injection", "A07:2021-Identification and Authentication Failures"],
        cwe: ["CWE-79", "CWE-94", "CWE-601"],
        tools: ["Semgrep", "ESLint security plugin", "Next.js security headers", "Retire.js"],
        detection_patterns: [
            "dangerouslySetInnerHTML",
            "eval(",
            "innerHTML",
            "document.write",
            "new Function("
        ],
        secure_coding: [
            "Never use dangerouslySetInnerHTML with user input",
            "Use React's built-in JSX escaping",
            "Implement Content Security Policy (CSP)",
            "Use HTTPOnly cookies for authentication",
            "Validate all server-side inputs"
        ],
        remediation: [
            "Enable CSP headers in next.config.js",
            "Use sanitize-html or DOMPurify for user content",
            "Implement rate limiting on API routes",
            "Use next-auth for authentication",
            "Enable security headers in middleware"
        ]
    },

    django: {
        name: "Django (Python)",
        icon: "🐍",
        category: "web_framework",
        vulnerabilities: [
            "SQL injection via raw queries",
            "Template injection (SSTI)",
            "CSRF bypass",
            "Mass assignment via ModelForm",
            "Debug mode in production",
            "Secret key exposure",
            "Email header injection",
            "Path traversal in file uploads"
        ],
        owasp_mapping: ["A03:2021-Injection", "A04:2021-Insecure Design"],
        cwe: ["CWE-89", "CWE-94", "CWE-352"],
        tools: ["Bandit", "Safety", "django-extensions", "nose"],
        detection_patterns: [
            "raw(",
            "extra(",
            "execute(",
            "mark_safe(",
            "DEBUG = True"
        ],
        secure_coding: [
            "Always use ORM queries instead of raw SQL",
            "Use Django's built-in template escaping",
            "Enable CSRF middleware",
            "Use ModelForms for data validation",
            "Keep DEBUG = False in production"
        ],
        remediation: [
            "Use django-csp for Content Security Policy",
            "Enable django-axes for brute-force protection",
            "Use django-secure for security headers",
            "Run Bandit in CI/CD pipeline",
            "Use environment variables for secrets"
        ]
    },

    spring: {
        name: "Spring Boot (Java)",
        icon: "🍃",
        category: "web_framework",
        vulnerabilities: [
            "Spring4Shell (CVE-2022-22965)",
            "SpEL injection",
            "Actuator endpoint exposure",
            "Deserialization vulnerabilities",
            "SQL injection via JPA",
            "XXE in XML parsers",
            "CORS misconfiguration",
            "Mass assignment via @RequestBody"
        ],
        owasp_mapping: ["A03:2021-Injection", "A05:2021-Security Misconfiguration"],
        cwe: ["CWE-94", "CWE-502", "CWE-611"],
        tools: ["SpotBugs", "OWASP Dependency Check", "Spring Boot Actuator", "Burp Suite"],
        detection_patterns: [
            "SpEL expression",
            "@RequestBody",
            "ObjectMapper.readValue",
            "XMLInputFactory",
            "/actuator/"
        ],
        secure_coding: [
            "Disable unnecessary Actuator endpoints",
            "Use parameterized queries with JPA",
            "Validate all @RequestBody inputs",
            "Restrict CORS origins",
            "Use Jackson with polymorphic type handling disabled"
        ],
        remediation: [
            "Update Spring Boot to latest version",
            "Enable Spring Security CSRF protection",
            "Use @Valid annotation for input validation",
            "Disable debug endpoints in production",
            "Use Snyk or OWASP Dependency Check"
        ]
    },

    // ═══════════════════════════════════════════════
    // MOBILE PLATFORMS
    // ═══════════════════════════════════════════════
    android: {
        name: "Android",
        icon: "🤖",
        category: "mobile",
        vulnerabilities: [
            "Insecure data storage (SharedPreferences)",
            "Insecure network communication",
            "Insufficient certificate validation",
            "Intent injection",
            "Content Provider leaks",
            "Root detection bypass",
            "Insecure deep links",
            "WebView JavaScript injection"
        ],
        owasp_mapping: ["A01:2021-Broken Access Control", "A02:2021-Cryptographic Failures"],
        cwe: ["CWE-312", "CWE-319", "CWE-927"],
        tools: ["MobSF", "Frida", "Objection", "Drozer", "APKTool"],
        detection_patterns: [
            "SharedPreferences",
            "MODE_WORLD_READABLE",
            "android:allowBackup=\"true\"",
            "usesCleartextTraffic"
        ],
        secure_coding: [
            "Use EncryptedSharedPreferences for sensitive data",
            "Enforce network security configuration",
            "Use certificate pinning",
            "Validate all Intent data",
            "Disable backup in production"
        ],
        remediation: [
            "Enable ProGuard/R8 code obfuscation",
            "Use Android Keystore for cryptographic keys",
            "Implement root detection",
            "Use Security Utils library",
            "Enable Google Play App Signing"
        ]
    },

    ios: {
        name: "iOS (Swift/Objective-C)",
        icon: "🍎",
        category: "mobile",
        vulnerabilities: [
            "Keychain misconfiguration",
            "Insecure URL handling (custom schemes)",
            "Jailbreak detection bypass",
            "Pasteboard data leakage",
            "Insecure UserDefaults storage",
            "App Transport Security bypass",
            "Runtime manipulation",
            "Binary patching"
        ],
        owasp_mapping: ["A02:2021-Cryptographic Failures", "A04:2021-Insecure Design"],
        cwe: ["CWE-312", "CWE-319", "CWE-522"],
        tools: ["Frida", "Objection", "class-dump", "Hopper", "iOS Security Suite"],
        detection_patterns: [
            "UserDefaults",
            "NSHomeDirectory",
            "UIApplicationOpenSettingsURLString",
            "canOpenURL",
            "HTTP (not HTTPS)"
        ],
        secure_coding: [
            "Use Keychain for sensitive data storage",
            "Enforce App Transport Security (ATS)",
            "Use Universal Links instead of custom URL schemes",
            "Implement jailbreak detection",
            "Use Data Protection API"
        ],
        remediation: [
            "Enable Swift compiler security features",
            "Use iOS Security Suite",
            "Implement certificate pinning",
            "Enable Code Signing Entitlements",
            "Use Xcode's built-in security analysis"
        ]
    },

    // ═══════════════════════════════════════════════
    // AI/ML PLATFORMS
    // ═══════════════════════════════════════════════
    langchain: {
        name: "LangChain / LLM Applications",
        icon: "🤖",
        category: "ai_ml",
        vulnerabilities: [
            "Prompt injection in LLM chains",
            "Tool abuse via LLM output",
            "Memory poisoning (conversation history)",
            "RAG data exfiltration",
            "Agent privilege escalation",
            "Model output manipulation",
            "API key exposure in chain config",
            "Unintended tool invocation"
        ],
        owasp_mapping: ["A03:2021-Injection", "A08:2021-Software and Data Integrity Failures"],
        cwe: ["CWE-77", "CWE-94", "CWE-502"],
        tools: ["LangSmith", "LangFuse", "Guardrails AI", "NeMo Guardrails", "Rebuff"],
        detection_patterns: [
            "Prompt template with user input",
            "Tool.from_function without validation",
            "ConversationBufferMemory with user content",
            "Retriever with untrusted data source",
            "Agent with excessive tools"
        ],
        secure_coding: [
            "Validate and sanitize all LLM inputs",
            "Use output parsers with schema validation",
            "Implement tool access controls",
            "Use guardrails for LLM output",
            "Limit agent tool access"
        ],
        remediation: [
            "Implement prompt firewalls",
            "Use structured output parsing",
            "Add input/output logging",
            "Implement rate limiting on LLM calls",
            "Use sandboxed execution for tools"
        ]
    },

    openai_api: {
        name: "OpenAI API",
        icon: "🧠",
        category: "ai_ml",
        vulnerabilities: [
            "System prompt extraction",
            "Function calling abuse",
            "Token limit manipulation",
            "Response manipulation via context",
            "API key exposure in logs",
            "Cost exhaustion attacks",
            "Data leakage via fine-tuning",
            "Model confusion attacks"
        ],
        owasp_mapping: ["A03:2021-Injection", "A05:2021-Security Misconfiguration"],
        cwe: ["CWE-200", "CWE-77", "CWE-400"],
        tools: ["Promptfoo", "LangSmith", "Helicone", "Portkey"],
        detection_patterns: [
            "system message with user input",
            "function_call with unvalidated args",
            "stream: true without content filtering",
            "temperature > 1.0",
            "max_tokens not set"
        ],
        secure_coding: [
            "Never expose system prompts to users",
            "Validate function call arguments",
            "Set appropriate token limits",
            "Use content moderation API",
            "Log all API interactions"
        ],
        remediation: [
            "Implement input/output filtering",
            "Use OpenAI's moderation endpoint",
            "Set spending limits on API keys",
            "Use environment variables for API keys",
            "Implement request rate limiting"
        ]
    },

    // ═══════════════════════════════════════════════
    // DATABASES
    // ═══════════════════════════════════════════════
    postgresql: {
        name: "PostgreSQL",
        icon: "🐘",
        category: "database",
        vulnerabilities: [
            "SQL injection via string concatenation",
            "Privilege escalation (SUPERUSER)",
            "pg_hba.conf misconfiguration",
            "Extension abuse (plpythonu, plperl)",
            "Backup file exposure",
            "Replication slot overflow",
            "Connection pool exhaustion",
            "pg_stat_statement data leakage"
        ],
        owasp_mapping: ["A03:2021-Injection", "A05:2021-Security Misconfiguration"],
        cwe: ["CWE-89", "CWE-284", "CWE-532"],
        tools: ["pgBadger", "pgAudit", "pgBouncer", "Nessus"],
        detection_patterns: [
            "EXECUTE IMMEDIATE",
            "COPY FROM PROGRAM",
            "pg_read_file",
            "dblink",
            "CREATE EXTENSION"
        ],
        secure_coding: [
            "Always use parameterized queries",
            "Use least-privilege database roles",
            "Enable SSL for connections",
            "Use pgAudit for audit logging",
            "Restrict superuser access"
        ],
        remediation: [
            "Enable row-level security (RLS)",
            "Configure pg_hba.conf properly",
            "Regular security patches",
            "Enable connection encryption",
            "Monitor pg_stat_activity"
        ]
    },

    mongodb: {
        name: "MongoDB",
        icon: "🍃",
        category: "database",
        vulnerabilities: [
            "NoSQL injection via $where",
            "Operator injection ($gt, $ne, $regex)",
            "Aggregation pipeline injection",
            "GridFS file exposure",
            "MongoDB Compass default config",
            "Replica set compromise",
            "MongoDB Atlas IAM misconfiguration",
            "BSON injection"
        ],
        owasp_mapping: ["A03:2021-Injection", "A01:2021-Broken Access Control"],
        cwe: ["CWE-943", "CWE-284", "CWE-601"],
        tools: ["NoSQLMap", "MongoDB Atlas CLI", "mongodump"],
        detection_patterns: [
            "$where",
            "$gt",
            "$ne",
            "$regex",
            "eval(",
            "db.collection.find({$where:"
        ],
        secure_coding: [
            "Never use $where with user input",
            "Use Mongoose schema validation",
            "Enable authentication (SCRAM-SHA-256)",
            "Use TLS for connections",
            "Implement field-level encryption"
        ],
        remediation: [
            "Enable MongoDB Atlas network access controls",
            "Use MongoDB Encryption at Rest",
            "Enable audit logging",
            "Use MongoDB Database Users with least privilege",
            "Enable MongoDB Trigger for anomaly detection"
        ]
    },

    // ═══════════════════════════════════════════════
    // DEVOPS / CI/CD
    // ═══════════════════════════════════════════════
    github_actions: {
        name: "GitHub Actions",
        icon: "⚙️",
        category: "devops",
        vulnerabilities: [
            "Secrets exposure in logs",
            "Pull request target workflow abuse",
            "Reusable workflow injection",
            "GITHUB_TOKEN privilege escalation",
            "Dependency confusion attacks",
            "Action injection via PR titles",
            "Cache poisoning",
            "Environment variable leakage"
        ],
        owasp_mapping: ["A08:2021-Software and Data Integrity Failures", "A05:2021-Security Misconfiguration"],
        cwe: ["CWE-502", "CWE-284", "CWE-532"],
        tools: ["Gitleaks", "TruffleHog", "StepSecurity", "ActionLint"],
        detection_patterns: [
            "pull_request_target",
            "${{ github.event",
            "secrets.GITHUB_TOKEN",
            "run: ${{",
            "uses: ./.github/workflows"
        ],
        secure_coding: [
            "Never echo secrets in logs",
            "Use pull_request instead of pull_request_target",
            "Pin actions to specific SHA",
            "Use GITHUB_TOKEN with minimal permissions",
            "Validate PR content before processing"
        ],
        remediation: [
            "Enable required workflow reviews",
            "Use OIDC for cloud deployments",
            "Implement branch protection rules",
            "Use GitHub Advanced Security",
            "Audit action dependencies regularly"
        ]
    },

    docker: {
        name: "Docker / Containers",
        icon: "🐳",
        category: "devops",
        vulnerabilities: [
            "Running as root in containers",
            "Exposed Docker socket",
            "Secrets in image layers",
            "Privileged container escape",
            "Container drift (mutable images)",
            "Registry credential exposure",
            "Network namespace bypass",
            "Supply chain attacks via base images"
        ],
        owasp_mapping: ["A05:2021-Security Misconfiguration", "A08:2021-Software and Data Integrity Failures"],
        cwe: ["CWE-250", "CWE-284", "CWE-502"],
        tools: ["Trivy", "Snyk Container", "Grype", "Docker Bench Security", "Falco"],
        detection_patterns: [
            "FROM.*:latest",
            "USER root",
            "RUN.*sudo",
            "EXPOSE 2375",
            "volume: /var/run/docker.sock"
        ],
        secure_coding: [
            "Use non-root USER in Dockerfile",
            "Use multi-stage builds",
            "Scan images for vulnerabilities",
            "Pin base image versions",
            "Use .dockerignore"
        ],
        remediation: [
            "Enable Docker Content Trust",
            "Use read-only file systems",
            "Limit container resources",
            "Use seccomp profiles",
            "Enable runtime security monitoring"
        ]
    },

    // ═══════════════════════════════════════════════
    // SOCIAL / MESSAGING
    // ═══════════════════════════════════════════════
    whatsapp_business: {
        name: "WhatsApp Business API",
        icon: "💬",
        category: "messaging",
        vulnerabilities: [
            "Webhook URL exposure",
            "Message template injection",
            "Media URL SSRF",
            "Phone number enumeration",
            "Business verification bypass",
            "Rate limiting bypass",
            "End-to-end encryption key management",
            "Third-party integration data leak"
        ],
        owasp_mapping: ["A01:2021-Broken Access Control", "A03:2021-Injection"],
        cwe: ["CWE-918", "CWE-79", "CWE-319"],
        tools: ["WhatsApp Business API Toolkit", "Postman Collection"],
        detection_patterns: [
            "webhook_url",
            "message.template",
            "media_url",
            "phone_number",
            "Bearer token"
        ],
        secure_coding: [
            "Validate webhook signatures",
            "Use HTTPS for webhook URLs",
            "Sanitize message templates",
            "Implement rate limiting",
            "Use environment variables for tokens"
        ],
        remediation: [
            "Enable two-factor authentication",
            "Regular API key rotation",
            "Monitor API usage logs",
            "Implement IP whitelisting for webhooks",
            "Use WhatsApp Business Management API for security"
        ]
    },

    telegram: {
        name: "Telegram Bot API",
        icon: "✈️",
        category: "messaging",
        vulnerabilities: [
            "Bot token exposure",
            "Webhook URL injection",
            "Callback data manipulation",
            "Inline query XSS",
            "File download path traversal",
            "Group admin privilege escalation",
            "Payment API abuse",
            "Bot command injection"
        ],
        owasp_mapping: ["A03:2021-Injection", "A07:2021-Identification and Authentication Failures"],
        cwe: ["CWE-79", "CWE-22", "CWE-284"],
        tools: ["Telebot", "Aiogram", "python-telegram-bot"],
        detection_patterns: [
            "bot_token",
            "webhook_url",
            "callback_data",
            "inline_query",
            "file_id"
        ],
        secure_coding: [
            "Never expose bot tokens in code",
            "Validate callback data server-side",
            "Sanitize inline query results",
            "Use HTTPS for webhook URLs",
            "Implement rate limiting on bot commands"
        ],
        remediation: [
            "Use environment variables for tokens",
            "Implement webhook IP whitelisting",
            "Enable bot privacy mode",
            "Validate all user inputs",
            "Use Telegram's built-in security features"
        ]
    }
};

// Platform categories for the UI
const PLATFORM_CATEGORIES = {
    cloud: { name: "Cloud Providers", icon: "☁️", platforms: ["aws", "azure", "gcp"] },
    web_framework: { name: "Web Frameworks", icon: "🌐", platforms: ["react", "django", "spring"] },
    mobile: { name: "Mobile Platforms", icon: "📱", platforms: ["android", "ios"] },
    ai_ml: { name: "AI / ML", icon: "🤖", platforms: ["langchain", "openai_api"] },
    database: { name: "Databases", icon: "🗄️", platforms: ["postgresql", "mongodb"] },
    devops: { name: "DevOps / CI/CD", icon: "⚙️", platforms: ["github_actions", "docker"] },
    messaging: { name: "Social / Messaging", icon: "💬", platforms: ["whatsapp_business", "telegram"] }
};
