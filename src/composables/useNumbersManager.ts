function useNumbersManager() {
  function createNextNumber(idList: Set<number>) {
    const maxId = idList.size > 0 ? Math.max(...idList.values()) : 0;
    return maxId + 1;
  }

  function isNumberOnTheList(idList: Set<number>, idToCheck: number) {
    return idList.has(idToCheck);
  }

  return {
    createNextNumber,
    isNumberOnTheList
  }
}

export default useNumbersManager()
