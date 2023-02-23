./launchDocker.sh ./SubjectFiles/s_JestSubjects.csv 10 --stress |& tee missed_subjects_s.log

./launchDocker.sh ./SubjectFiles/ns_JestsSubjects.csv 10 --no_stress |& tee missed_subjects_ns.log