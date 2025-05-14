import ProfileForm from '@/components/profile/profile-form';
import { useTitle } from '@/hooks/useTitle';
export default function Profile() {
  useTitle('Profile');
  return <ProfileForm />;
}
