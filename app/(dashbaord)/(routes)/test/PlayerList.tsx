import playersNames from '../../../../public/players_data.json';


const PlayerList = async ({query} : {query: string}) => {

  

  const fullNames = playersNames.map((player) => player.full_name);

  const filterPlayers = Array.isArray(fullNames) ? fullNames.filter((player)=>{
    return player.toLowerCase().includes(query.toLowerCase());
  }) : [];

  console.log(filterPlayers)
  return (
    <div></div>

  )
}

export default PlayerList
