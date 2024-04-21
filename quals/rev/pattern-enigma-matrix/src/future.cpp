#include <ctre.hpp>
#include <iostream>
#include <string>

int main(int argc, char *argv[])
{
	if (argc < 2)
	{
		std::cout << argv[0] << "{flag_guess}" << std::endl;
		return 1;
	}
	auto flag = argv[1];
	std::cout << "Your Guess: '" << flag << "'" << std::endl;
	bool constraints[] = {
		ctre::search<"m4tch">(flag),
		ctre::search<"1nG">(flag),
		ctre::search<"1m3">(flag),
		ctre::search<"t1m">(flag),
		ctre::search<"c0mp">(flag),
		ctre::search<"1le">(flag),
		ctre::search<"ef6f33a17d0b9c\\}$">(flag),
		ctre::search<"^grey\\{">(flag),
		ctre::match<"^.{68}$">(flag),
		ctre::search<"[def]{4}669870fc2fec[a-f0-9]{16}">(flag),
		ctre::search<"[a-z0-9]{7}_[a-z0-9]{4}_[a-z0-9]{7}_[a-zG0-9]{8}_[a-f0-9]{32}">(flag),
	};

	size_t arrLen = sizeof(constraints);
	for (int i = 0; i < arrLen; ++i)
	{
		if (!constraints[i])
		{
			std::cout << "Wrong flag! " << i << "/" << arrLen << " cases passed" << std::endl;
			return 1;
		}
	}

	std::cout << "Correct Flag!" << std::endl;
	return 0;
}