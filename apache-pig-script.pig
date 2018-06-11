--load positive words, keep only lines that start with word characters ([a-zA-Z_0-9]), add score column of 1's
positive_words = LOAD '/root/competition4/input/positive.txt' AS (word:charArray);
positive_words = FILTER positive_words BY NOT (word MATCHES '^;.*');	--filter out comment lines which start with ';'
positive_words = FOREACH positive_words GENERATE *, 1 as positiveScore;
DESCRIBE positive_words;
DUMP positive_words;

--load negative words, keep only lines that start with word characters ([a-zA-Z_0-9]), add score column of 1's
negative_words = LOAD '/root/competition4/input/negative.txt' AS (word:charArray);
negative_words = FILTER negative_words BY NOT (word MATCHES '^;.*');	--filter out comment lines which start with ';'
negative_words = FOREACH negative_words GENERATE *, 1 as negativeScore;
DESCRIBE negative_words;
DUMP negative_words;

-- load reviews
reviews = LOAD '/root/competition4/input/sampleReviewData_mod_2.txt' USING PigStorage('\t') 
AS (memberID:chararray, productID:chararray, date:chararray, numHelpfulFeedbacks:int, 
numFeedbacks:int, rating:double, title:chararray, body:chararray);

-- keep only productID, title, body columns, remove punctuation
reviews = FOREACH reviews GENERATE productID, title, LOWER(REPLACE(body, '[^a-zA-Z0-9-+]', ' ')) as body;
DESCRIBE reviews;
DUMP reviews;

-- tokenize words
reviews_tokenized = FOREACH reviews GENERATE productID, title, FLATTEN(TOKENIZE(body)) as bodyWord;
DESCRIBE reviews_tokenized;
DUMP reviews_tokenized;

-- join review words to words from negative and positive columns
result = JOIN reviews_tokenized BY bodyWord LEFT OUTER, positive_words BY word;
result = JOIN result BY bodyWord LEFT OUTER, negative_words BY word;
result = FOREACH result GENERATE reviews_tokenized::productID AS productID, reviews_tokenized::title AS title,
reviews_tokenized::bodyWord as word,
(positive_words::positiveScore IS NOT NULL ? positive_words::positiveScore : 0) as positiveScore,
(negative_words::negativeScore IS NOT NULL ? negative_words::negativeScore : 0) as negativeScore;

-- count # of positive and negative words for each review
result_grouped = GROUP result BY (productID, title);

-- count number of positive and negative words in each review
result_count = FOREACH result_grouped GENERATE FLATTEN(group) AS (productID, title), 
SUM(result.positiveScore) AS positiveCount, SUM(result.negativeScore) AS negativeCount;
DESCRIBE result_count;
DUMP result_count;

-- classify each review as "positive" or "negative" or "neutral"
reviews_classified = FOREACH result_count 
GENERATE productID, (positiveCount > negativeCount ? 'positive' : (positiveCount == negativeCount ? 'neutral' : 'negative')) as class;
DESCRIBE reviews_classified;
DUMP reviews_classified;

-- filter and count positive reviews, group by productID
positive_reviews = FILTER reviews_classified BY class == 'positive';
positive_reviews_grouped = GROUP positive_reviews BY productID;
positive_reviews_counted = FOREACH positive_reviews_grouped 
GENERATE group as productID_P, COUNT(positive_reviews.class) as numPositiveReviews;
DESCRIBE positive_reviews_counted;
DUMP positive_reviews_counted;

-- filter and count negative or neutral reviews, group by productID
negative_or_neutral_reviews = FILTER reviews_classified BY (class == 'negative' or class == 'neutral');
negative_or_neutral_reviews_grouped = GROUP negative_or_neutral_reviews BY productID;
negative_or_neutral_reviews_counted = FOREACH negative_or_neutral_reviews_grouped 
GENERATE group as productID_N, COUNT(negative_or_neutral_reviews.class) as numNegativeOrNeutralReviews;
DESCRIBE negative_or_neutral_reviews_counted;
DUMP negative_or_neutral_reviews_counted;

-- join positive and negative and neutral review counts, output total # of reviews and percentage positive reviews per productID, sort by ascending productID
all_reviews = JOIN positive_reviews_counted BY productID_P FULL OUTER, negative_or_neutral_reviews_counted BY productID_N;
all_reviews = FOREACH all_reviews GENERATE (productID_P IS NOT NULL ? productID_P : productID_N) as productID, 
(numPositiveReviews IS NOT NULL ? numPositiveReviews : 0) as numPositiveReviews, 
(numNegativeOrNeutralReviews IS NOT NULL ? numNegativeOrNeutralReviews : 0) as numNegativeOrNeutralReviews;
DESCRIBE all_reviews;
DUMP all_reviews;
all_reviews = FOREACH all_reviews GENERATE productID, (numNegativeOrNeutralReviews + numPositiveReviews) AS totalCount, 
(float)((float)((float)numPositiveReviews / (numNegativeOrNeutralReviews + numPositiveReviews)) * 100) as positivePercentage;
all_reviews = ORDER all_reviews by productID ASC;
DESCRIBE all_reviews;
DUMP all_reviews;

STORE all_reviews INTO '/root/competition4/output/resultSampleFile' USING PigStorage('\t');
