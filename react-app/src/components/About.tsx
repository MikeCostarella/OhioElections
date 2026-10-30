import { SOS } from "../data/load";

export default function About({ loadedCounties }: { loadedCounties: string[] }) {
  return (
    <div className="about">
      <h2>What this is</h2>
      <p>What is on the ballot in each Ohio county, and later how it came out: candidates, the statewide issue, and the local tax levies, questions and liquor options. It is the third piece alongside the county <b>Voters</b> apps (who is registered and who voted) and <b>Current Election Statistics</b> (the early vote, rolled up statewide).</p>
      <h2>Where the data comes from</h2>
      <ul>
        <li>Statewide races and issues: from the Board of Elections' election notice (Secretary of State Form 120), which every county posts.</li>
        <li>County and local races and issues: from that county's Board of Elections' candidate list, issues list and election notice. Every entry links to the document it came from.</li>
        <li>Counties with local data so far: <b>{loadedCounties.length ? loadedCounties.join(", ") : "none"}</b>. Other counties show the statewide ballot and a link to their Board.</li>
      </ul>
      <h2>How it is presented</h2>
      <ul>
        <li>Candidates are listed alphabetically by last name. Ohio rotates the order of names from precinct to precinct, so there is no single "ballot order".</li>
        <li>Clicking a candidate's name opens a Google search for that person in a new tab. Google's results are not part of this app.</li>
        <li>Party labels are exactly as the Board prints them. Common pleas judges carry no party label on Ohio's general-election ballot.</li>
        <li>No ratings, endorsements or commentary. Issue wording is the Board's.</li>
        <li>Picking your city, village or township narrows the list to what that place votes on. Issues follow precinct lines, so for your exact ballot use your county's ballot lookup or the <a href={SOS.sampleBallot} target="_blank" rel="noopener noreferrer">Secretary of State's sample-ballot page</a>.</li>
      </ul>
      <h2>Corrections</h2>
      <p>If something here differs from your Board of Elections, the Board is right. Please email <a href="mailto:Mike.Costarella@gmail.com">Mike.Costarella@gmail.com</a>.</p>
      <p className="muted">This is a community reference tool, not an official government site.</p>
    </div>
  );
}
