"use client"
import playersNames from '../../../../public/players_data.json';


const PlayerList = async ({query} : {query: string}) => {

  

  const fullNames = playersNames.map((player) => player.full_name);

  const filterPlayers = Array.isArray(fullNames) ? fullNames.filter((player)=>{
    return player.toLowerCase().includes(query.toLowerCase());
  }) : [];

  const handleClick = (player : string) =>{
    console.log(`Clicked on player: ${player}`);
  };

  return (
    <div>
      {Array.isArray(fullNames) && fullNames.length === 0 && (
        <p className='mt-4'> No player found</p>
      )}

      <div className='flex flex-col mt-6'>

        {Array.isArray(fullNames) && 
          filterPlayers.map((player) =>(
          <div
            key ={player}
            className='flex flex-col cursor-pointer'
            onClick={() => handleClick(player)}
            >
              <div className='flex space-x-6 items-center'>
                <h2 className=''>{player}</h2>
              </div>

          </div>
        ))}
      </div>

    </div>

  )
}

export default PlayerList
