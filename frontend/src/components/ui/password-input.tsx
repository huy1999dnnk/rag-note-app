import * as React from 'react';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { cn } from '@/lib/utils';
import { Button } from './button';
import { Input } from '@/components/ui/input';

interface PasswordInputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const PasswordInput = React.forwardRef<HTMLInputElement, PasswordInputProps>(
  ({ className, ...props }, ref) => {
    const [showPassword, setShowPassword] = React.useState(false);

    return (
      <div className="relative">
        <Input
          type={showPassword ? 'text' : 'password'}
          className={cn('pr-10', className)}
          ref={ref}
          {...props}
        />
        <Button
          type="button"
          variant="ghost"
          size="sm"
          className="absolute right-0 top-0 h-full px-3 py-1 hover:bg-transparent"
          onClick={() => setShowPassword(!showPassword)}
          tabIndex={-1}
        >
          {showPassword ? (
            <FaEyeSlash className="h-4 w-4 text-muted-foreground" />
          ) : (
            <FaEye className="h-4 w-4 text-muted-foreground" />
          )}
          <span className="sr-only">{showPassword ? 'Hide password' : 'Show password'}</span>
        </Button>
      </div>
    );
  }
);

PasswordInput.displayName = 'PasswordInput';

export { PasswordInput };
