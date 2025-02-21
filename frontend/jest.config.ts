import { Config } from 'jest';
import { pathsToModuleNameMapper } from 'ts-jest';
import tsconfig from './tsconfig.json';


const additionalMapping = {
  '^services/(.*)$': '<rootDir>/src/services/$1',
  '^composables/(.*)$': '<rootDir>/src/composables/$1',
  '^enums/(.*)$': '<rootDir>/src/enums/$1',
};

const config: Config = {
  clearMocks: true,
  extensionsToTreatAsEsm: ['.ts'],
  moduleNameMapper: {
    ...additionalMapping,
    ...pathsToModuleNameMapper(tsconfig.compilerOptions.paths, { prefix: '<rootDir>/src' }),
  },
  preset: 'jest-preset-angular',
  setupFilesAfterEnv: ['<rootDir>/setup-jest.ts'],
};

export default config;
