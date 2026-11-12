# Safety, data protection and consent by design

## Clinical safety
- **Earlier, never later.** The personal trigger is capped at the WHO 300 ml line and the WHO rule always applies (`share/thresholds.py`, tested).
- **Human in charge.** Alerts are prompts. Compression starts only after staff confirm PPH (`share/compression.py`, tested).
- **Compression interlocks.** Runs only on a soft uterus; pressure cap; deflates on stop, fault or power loss; one-button stop.
- **Explainable alerts.** Every risk level lists the factors behind it.
- **Fair across skin tones.** No optical sensors. Signal quality will be tested across body types.
- **Hygiene.** The belt touches intact skin only (a non-critical item under Spaulding). Skin liner, electrode pads and pad sleeve are single-use; sensors and hub are sealed and wipe-clean.

## Data protection
- Kenya Data Protection Act 2019 and the Pharmacy and Poisons Board guidance on medical device software.
- Informed consent from every mother in any study, in a language she understands.
- Data minimisation: only signals and fields the model needs; no names on the device.
- Pseudonymised IDs; data stored in Kenya; encrypted at rest and in transit.
- The device works offline; logs sync later for audit only.
- No real patient data is ever committed to this repository.

## Standards we are working towards
ISO 13485 (quality), ISO 14971 (risk), IEC 60601-1 and 60601-1-2 (electrical safety, EMC), IEC 62304 (software lifecycle), IEC 62366-1 (usability), ISO 10993 (skin contact), Good Machine Learning Practice.

## Reporting a safety concern
Open an issue labelled `safety`, or contact the maintainers privately.
