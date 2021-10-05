CREATE TABLE reports(
	id integer PRIMARY KEY AUTOINCREMENT,
	CIK text NOT NULL,
	ticker text NOT NULL,
	company_name text NOT NULL,
	exchange text,
	report_period text,
	filing_date text,
	source_url text,
	file_directory text	
	);

