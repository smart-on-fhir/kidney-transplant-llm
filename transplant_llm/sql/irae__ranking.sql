create TABLE irae__ranking as select * from (values

-- All Infection Type Rankings
 ('infection', 'Confirmed', 3)
,('infection', 'Treatment', 2)
,('infection', 'Suspected', 1)
,('infection', 'NoneOfTheAbove', 0)

-- Graft Rejection includes BiopsyProven
,('rejection', 'BiopsyProven', 4)
,('rejection', 'Confirmed', 3)
,('rejection', 'Treatment', 2)
,('rejection', 'Suspected', 1)
,('rejection', 'NoneOfTheAbove', 0)

-- Graft Failure, no treatment case (study endpoint)
,('failure', 'Confirmed', 3)
,('failure', 'Suspected', 1)
,('failure', 'NoneOfTheAbove', 0)

-- Cancer including PTLD (Lymphoma)
,('cancer', 'BiopsyProven', 4)
,('cancer', 'Treatment', 2)
,('cancer', 'Suspected', 1)


-- Donor Characteristics
,('donor', 'Living', 1)
,('donor', 'Deceased', -1)
,('donor', 'NotMentioned', 0)

,('donor', 'Related', 1)
,('donor', 'Unrelated', -1)
,('donor', 'NotMentioned', 0)

-- HLA Match Quality
,('hla', 'Well', 6-1)
,('hla', 'Moderate', 6-3)
,('hla', 'Poor', 6-5)
,('hla', 'NotMentioned', 0)

-- HLA Mismatches (6 minus #mismatched)
,('hla', 'Zero', 6)
,('hla', 'One', 6-1)
,('hla', 'Two', 6-2)
,('hla', 'Three', 6-3)
,('hla', 'Four', 6-4)
,('hla', 'Five', 6-5)
,('hla', 'Six', 6-6)
,('hla', 'NotMentioned', 0)

-- Especially medication compliance and drug therapeutic dosing                                                             
,('documented', 'DocumentedTrue', 1)
,('documented', 'DocumentedFalse', -1)
,('documented', 'NotMentioned', 0)

) AS t (topic, code, ranking) ;