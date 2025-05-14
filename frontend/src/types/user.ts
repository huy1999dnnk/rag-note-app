export interface IUpdateUserProfile {
  username: string | undefined | null;
  current_password: string | null | undefined;
  new_password: string | null | undefined;
  type_auth: 'social' | 'local';
}
