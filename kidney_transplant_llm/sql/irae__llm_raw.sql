CREATE EXTERNAL TABLE irae__gpt4_raw
(
    patient_id      string,
    docref_dxr_id   string,

    donor_transplant_date_value             date,
    donor_transplant_date_mention           boolean,
    donor_transplant_date_spans_valid       boolean,
    donor_transplant_date_spans_formatted   string,

    donor_type_value            string,
    donor_type_mention          boolean,
    donor_type_spans_valid      boolean,
    donor_type_spans_formatted  string,

    donor_relationship_value            string,
    donor_relationship_mention          boolean,
    donor_relationship_spans_valid      boolean,
    donor_relationship_spans_formatted  string,

    donor_hla_match_quality_value           string,
    donor_hla_match_quality_mention         boolean,
    donor_hla_match_quality_spans_valid     boolean,
    donor_hla_match_quality_spans_formatted string,

    donor_hla_mismatch_count_value              string,
    donor_hla_mismatch_count_mention            boolean,
    donor_hla_mismatch_count_spans_valid        boolean
    donor_hla_mismatch_count_spans_formatted    string,

    rx_therapeutic_status_value             string,
    rx_therapeutic_status_mention           boolean,
    rx_therapeutic_status_spans_valid       boolean,
    rx_therapeutic_status_spans_formatted   string,

    rx_compliance_value             string,
    rx_compliance_mention           boolean,
    rx_compliance_spans_valid       boolean,
    rx_compliance_spans_formatted   string,

    dsa_value           string,
    dsa_mention         boolean,
    dsa_mention_history boolean,
    dsa_spans_valid     boolean,
    dsa_spans_formatted string,

    infection_value             string,
    infection_mention           boolean,
    infection_mention_history   boolean,
    infection_spans_valid       boolean,
    infection_spans_formatted   string,

    viral_infection_value           string,
    viral_infection_mention         boolean,
    viral_infection_mention_history boolean,
    viral_infection_spans_valid     boolean,
    viral_infection_spans_formatted string,

    bacterial_infection_value           string,
    bacterial_infection_mention         boolean,
    bacterial_infection_mention_history boolean,
    bacterial_infection_spans_valid     boolean,
    bacterial_infection_spans_formatted string,

    fungal_infection_value              string,
    fungal_infection_mention            boolean,
    fungal_infection_mention_history    boolean,
    fungal_infection_spans_valid        boolean,
    fungal_infection_spans_formatted    string,

    graft_rejection_value               string,
    graft_rejection_mention             boolean,
    graft_rejection_mention_history     boolean,
    graft_rejection_spans_valid         boolean,
    graft_rejection_spans_formatted     string,

    graft_failure_value                 string,
    graft_failure_mention               boolean,
    graft_failure_mention_history       boolean,
    graft_failure_spans_valid           boolean,
    graft_failure_spans_formatted       string,

    ptld_value              string,
    ptld_mention            boolean,
    ptld_mention_history    boolean,
    ptld_spans_valid        boolean,
    ptld_spans_formatted    string,

    cancer_value            string,
    cancer_mention          boolean,
    cancer_mention_history  boolean,
    cancer_spans_valid      boolean,
    cancer_spans_formatted  string,

    deceased_value              string
    deceased_date               date,
    deceased_mention            boolean,
    deceased_spans_valid        boolean,
    deceased_spans_formatted    string
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION 's3://cumulus-analytics/andy/irae/llm/2025-10-16-donor-characteristics/'
--LOCATION 's3://cumulus-analytics/andy/irae/llm/2025-10-16-non-donor-characteristics/'
TBLPROPERTIES ("skip.header.line.count"="1");

