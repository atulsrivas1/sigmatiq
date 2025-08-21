import React from 'react';
import styled from 'styled-components';
import { theme } from '../../styles/theme';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  size?: 'small' | 'medium' | 'large';
  onClick?: () => void;
  fullWidth?: boolean;
  className?: string;
}

const StyledButton = styled.button<ButtonProps>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: ${props => 
    props.size === 'small' ? '6px 14px' :
    props.size === 'large' ? '12px 20px' :
    '10px 16px'
  };
  background: ${props => 
    props.variant === 'primary' 
      ? theme.colors.primary.brightTeal 
      : theme.colors.bg.surface2
  };
  border: 1px solid ${props => 
    props.variant === 'primary' 
      ? theme.colors.primary.brightTeal 
      : theme.colors.bg.border
  };
  border-radius: ${theme.borderRadius.md};
  color: ${props => 
    props.variant === 'primary' 
      ? theme.colors.bg.primary 
      : theme.colors.text.primary
  };
  font-weight: 500;
  font-size: ${props => props.size === 'small' ? '12px' : '13px'};
  cursor: pointer;
  transition: all 0.2s;
  width: ${props => props.fullWidth ? '100%' : 'auto'};

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  }
`;

export const Button: React.FC<ButtonProps> = ({ 
  children, 
  variant = 'secondary', 
  size = 'medium', 
  onClick,
  fullWidth = false,
  className 
}) => {
  return (
    <StyledButton 
      variant={variant} 
      size={size} 
      onClick={onClick}
      fullWidth={fullWidth}
      className={className}
    >
      {children}
    </StyledButton>
  );
};
