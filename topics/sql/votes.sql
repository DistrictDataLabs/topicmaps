WITH topic_votes AS (
  SELECT t.id, t.title, t.is_canonical, t.refers_to_id, SUM(v.vote) as votes
    FROM topics t
    JOIN voting v on v.topic_id = t.id
    GROUP BY t.id, t.title, t.is_canonical, t.refers_to_id
   )
SELECT cv.id, cv.title, (coalesce(sum(ncv.votes), 0) + cv.votes) AS vote_total
  FROM topic_votes cv
  LEFT OUTER JOIN topic_votes ncv on cv.id = ncv.refers_to_id
  WHERE cv.is_canonical = TRUE
  GROUP BY cv.id, cv.title, cv.votes
  ORDER BY vote_total DESC, title
;
