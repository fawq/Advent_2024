module Part2 where

import Data.Function (fix)
import System.IO (readFile)

getNumberOfDigits :: Int -> Int
getNumberOfDigits number = length $ show number

getNumberOfStones :: (Int -> Int -> Int) -> Int -> Int -> Int
getNumberOfStones f _ 0 = 1
getNumberOfStones f number iterations
  | number == 0 = f 1 (iterations - 1)
  | even $ getNumberOfDigits number = let (firstHalf, secondHalf) = splitAt (length (show number) `div` 2) (show number)
                                       in f (read firstHalf) (iterations - 1) + f (read secondHalf) (iterations - 1)
  | otherwise = f (number * 2024) (iterations - 1)

memoize :: (Int -> a) -> (Int -> a)
memoize f = (map f [0 ..] !!)

getNumberOfStonesMemoized :: Int -> Int -> Int
getNumberOfStonesMemoized = fix (memoize . getNumberOfStones)

solution :: FilePath -> IO Int
solution filePath = do
  contents <- readFile filePath
  let numbers = map read $ words contents
  return $ sum $ map (`getNumberOfStonesMemoized` 75) numbers

main :: IO ()
main = do
    result <- solution "data.txt"
    print result