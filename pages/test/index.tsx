//server component 
import SearchPlayers from "./SearchPlayers";
import PlayerList from "./PlayerList";

const SearchPage = ({
  searchParams
}:{
  searchParams?: {
    query?: string; //optional becusae someonoen might not actually type anyhting into the input 
  };
}) => {
  const query = searchParams?.query || ``;

  // console.log("query", query);
  return (
    <div>
      <h1>Search Player Here: </h1>
      <SearchPlayers />
      <PlayerList query={query} />
    </div>
  )
}

export default SearchPage
