# Clearview Health Plans — Engineering Onboarding

Welcome to Claims Engineering. This doc should get you oriented enough to not be completely lost in your first week. It's not comprehensive — ask questions, people are generally helpful.

## What We Do

Clearview is a regional health insurer. We cover about 800K members across three states. The core of what engineering supports is the claims processing pipeline: a provider renders services to a member, submits a claim, we figure out what's covered under the member's plan, and we pay the provider (or deny the claim, or hold it for review). That's the business in one sentence.

## The Big Systems

**Claims Gateway** — this is where everything comes in. EDI 837 files from clearinghouses, JSON submissions from our portal, even paper claims that go through OCR. It validates format, checks for duplicates, and routes claims downstream. If you hear someone say "the gateway is backed up" they mean this.

**Rules Engine** — the adjudication brain. It's a vendor product (we're mid-migration to replace it, long story). Takes a validated claim and runs it against benefit plan rules, fee schedules, medical policy edits, the works. Spits out a disposition: pay, deny, or pend for manual review.

**Eligibility Service** — source of truth for member enrollment. Handles the 270/271 EDI transactions. Also tracks accumulators (how much of your deductible you've met, OOP max progress). The rules engine checks this during adjudication.

**Payment Engine** — takes adjudicated claims and turns them into money. Provider payments via EFT, member reimbursements, ERA 835 remittance advice. Also handles void/reissue when we mess up.

**Pre-Auth Service** — manages prior authorization requests. Providers submit auth requests, we auto-approve the routine ones (~60% target) and route complex cases to clinical reviewers.

**Fraud Detection** — ML models that score claims at intake (pre-payment) and analyze patterns after payment. Anything scoring above 0.82 gets held for SIU review. We retrain models monthly.

**Member Portal** — the consumer-facing app. Claims status, benefit balances, provider search, EOBs, digital ID cards. Member Services team owns it.

**Provider Directory** — master data for all contracted providers. Demographics, credentials, network status, fee schedules. Provider Network team keeps this current. (I think there's also something about credentialing workflows tied to this but honestly I'm not sure who owns that — ask James.)

## Teams

- **Claims Operations** — owns the pipeline end-to-end (gateway, rules engine, payment engine, fraud, pre-auth)
- **Member Services** — owns member portal and eligibility service
- **Provider Network** — owns provider directory, handles credentialing and contracting

## Jargon You'll Hear

- **Adjudication** — the process of evaluating a claim against plan rules to decide pay/deny/pend
- **EOB** — Explanation of Benefits, the document members get showing what was covered
- **COB** — Coordination of Benefits, when a member has coverage from multiple payers
- **NPI** — National Provider Identifier, the unique ID for healthcare providers
- **Allowed amount** — the max we'll pay for a service based on the provider's contract
- **Pend** — when a claim can't be auto-adjudicated and needs manual review

That should be enough to follow conversations. The architecture overview page has more detail on how the systems connect. Ask your team lead for access to the Confluence spaces.
