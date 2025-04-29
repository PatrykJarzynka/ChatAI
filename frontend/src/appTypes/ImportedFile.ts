export class ImportedFile {

  public selected: boolean;
  public fileName: string;

  constructor(fileName: string, selected: boolean) {
    this.fileName = fileName;
    this.selected = selected;
  }


  toggleSelection(): void {
    this.selected = !this.selected;
  }

}


