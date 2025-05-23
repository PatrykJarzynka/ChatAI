import { StatusType } from '@enums/StatusType';


export interface UploadedFile {
  id: number;
  name: string;
  status: StatusType;
}
