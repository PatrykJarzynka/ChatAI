import {describe, expect, test} from '@jest/globals';
import useNumbersManager from '../composables/useNumbersManager';


const { createNextNumber, isNumberOnTheList } = useNumbersManager;

describe('idManager', () => {
  test('create next id', () => {
    const idsSet = new Set([5,8,20,43,1]);

    const newId = createNextNumber(idsSet);

    expect(newId).toEqual(44);
  })

  test('is id already in list', () => {
    const idsSet = new Set([5,8,20,43,1]);

    const isIdOnTheList = isNumberOnTheList(idsSet, 8);

    expect(isIdOnTheList).toBeTruthy();
  })

  test('id is not on the list', () => {
    const idsSet = new Set([5,8,20,43,1]);

    const isIdOnTheList = isNumberOnTheList(idsSet, 29);

    expect(isIdOnTheList).toBeFalsy();
  })
})
