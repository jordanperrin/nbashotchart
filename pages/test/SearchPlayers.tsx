"use client"

import {MagnifyingGlassIcon} from "@heroicons/react/24/outline";
import { URLSearchParams } from "next/dist/compiled/@edge-runtime/primitives/url";
import {useSearchParams, usePathname, useRouter} from 'next/navigation'; 


const SearchPlayers = () => {

  const searchParams = useSearchParams(); //returns read only object
  const pathname = usePathname();
  const {replace} = useRouter();

  const handleSearch = (searchTerm: string) =>{
    const params = new URLSearchParams(searchParams); //this returns a mutabl object for the params so we can modify the search params
    if(searchTerm){
      params.set("query", searchTerm);
    }else{
      params.delete("query");
    }

    replace(`${pathname}?${params.toString()}`)
  }

  return (
    <div className="relative flex flex-1 flex-shrink-0">
      <label htmlFor="search" className="sr-only">
        Search
      </label>
      <input
        className="peer block w-1/2 rounded md border border-gray-200 py-[9px] pl-10 text-black text-sm outline-2 placeholder:text-gray-500"
        placeholder="search"
        defaultValue={searchParams.get('query')?.toString()}
        onChange = {(e) => {
          handleSearch(e.target.value);
        }}
      />
    <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900"/>
      
    </div>
  )
}

export default SearchPlayers
