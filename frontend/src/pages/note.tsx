import MainNote from '@/components/note/main-note';
import { useTitle } from '@/hooks/useTitle';
export default function Note() {
  useTitle('Note');
  return <MainNote />;
}
