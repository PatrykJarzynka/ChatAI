export class UniqueIdGenerator {
  private idCounter: number;
  private prefix: string;

  constructor(prefix: string = '') {
    this.idCounter = 0;
    this.prefix = prefix;
  }

  public generateId(): string {
    this.idCounter++;
    return `${this.prefix}_${this.idCounter}}`;
  }
}
