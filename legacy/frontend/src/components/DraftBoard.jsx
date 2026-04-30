import { useEffect, useState } from "react"


const DraftBoard = () => {
  const [draftResults, setDraftResults] = useState([]);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const res = await fetch("/pullDraftResults");
        const data = await res.json();
        setDraftResults(data.picks); // store the array of picks
        fetchResults();
      } catch (err) {
        console.error("Error fetching draft results:", err);
      }
    };

    fetchResults(); // only once on mount
  }, []);
  
  return (
    <div className="draftGrid">
      {draftResults.map((pick, index) => {
        const [username, info] = pick; // pick[0] = username, pick[1] = "Name | Pos | Team"
        return (
          <div key={index} className="draftBox">
            {username} ~ {info}
          </div>
        );
      })}
    </div>
  );
};

export default DraftBoard