import sys
from colorama import init, Fore, Style
import os

# Initialize colorama
init()

def convert_stex_to_png(input_filename):
    # Define output_filename early to ensure it's bound in exception handlers
    output_filename = input_filename + '-output.png'
    try:
        # Display processing message
        print(f"{Fore.CYAN}⚙️  Processing: {Fore.YELLOW}{input_filename}{Style.RESET_ALL}")

        with open(input_filename, 'rb') as input_file, open(output_filename, 'wb') as output_file:
            # 32 bits is based off the .stex header which are trimmed for png
            input_file.seek(32)

            # Get file size for progress tracking
            # Need to get the total size first, then subtract the header offset
            input_file_total_size = os.path.getsize(input_filename)
            if input_file_total_size < 32:
                 raise ValueError("Input file is too small to be a valid .stex file (less than 32 bytes).")
            file_size = input_file_total_size - 32
            input_file.seek(32) # Go back to position after header

            # Handle edge case where file size is exactly 32 bytes (no data after header)
            if file_size <= 0:
                print(f"\r{Fore.GREEN}▓{'░' * 10} 100%{Style.RESET_ALL}", end='', flush=True)
            else:
                # Copy data with progress indicator
                bytes_read = 0
                chunk_size = 1024
                while True:
                    # Read in chunks for better performance
                    chunk = input_file.read(chunk_size)
                    if not chunk:
                        break
                    output_file.write(chunk)

                    # Update progress
                    bytes_read += len(chunk)
                    # Ensure file_size is not zero before division
                    progress = min(100, int(bytes_read * 100 / file_size)) if file_size > 0 else 100
                    # Corrected progress bar logic
                    filled_bars = progress // 10
                    empty_bars = 10 - filled_bars
                    print(f"\r{Fore.GREEN}{'▓' * filled_bars}{Fore.WHITE}{'░' * empty_bars} {progress}%{Style.RESET_ALL}", end='', flush=True)

        print()  # New line after progress bar
        print(f"{Fore.GREEN}✅ Conversion successful: {Style.BRIGHT}{output_filename}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}ℹ️  Original: {Fore.YELLOW}{os.path.getsize(input_filename):,} bytes{Style.RESET_ALL}")
        print(f"{Fore.BLUE}ℹ️  Output: {Fore.YELLOW}{os.path.getsize(output_filename):,} bytes{Style.RESET_ALL}")

    except FileNotFoundError:
        print(f"{Fore.RED}❌ Error: File not found: {Fore.YELLOW}{input_filename}{Style.RESET_ALL}")
    except PermissionError:
        # output_filename is now guaranteed to be defined here
        print(f"{Fore.RED}❌ Error: Permission denied when writing to {Fore.YELLOW}{output_filename}{Style.RESET_ALL}")
    except ValueError as e:
        print(f"{Fore.RED}❌ Error: {Fore.YELLOW}{str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: An unexpected error occurred: {Fore.YELLOW}{str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        convert_stex_to_png(filename)
    else:
        print(f"{Fore.CYAN}🔍 {Style.BRIGHT}Godot STEX to PNG Converter{Style.RESET_ALL}")
        # The following line is syntactically correct Python, despite potential linter warnings.
        print(f"{Fore.WHITE}Usage: {Fore.YELLOW}python godotstex2png.py input.stex{Style.RESET_ALL}")
        print(f"{Fore.WHITE}This tool converts Godot's .stex files (stripping the first 32 bytes) to standard PNG images.{Style.RESET_ALL}")
