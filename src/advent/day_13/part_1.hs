import Data.List (stripPrefix)
import Data.Maybe (fromJust)
import qualified Data.Text as T
import qualified Data.Text.IO as TIO
import Debug.Trace (trace)
import Control.Monad (when)

data Equation = Equation
  { a1 :: Int
  , a2 :: Int
  , b1 :: Int
  , b2 :: Int
  , c1 :: Int
  , c2 :: Int
  } deriving (Show)

solution :: FilePath -> IO Int
solution filePath = do
  contents <- TIO.readFile filePath
  let lines' = T.lines contents
      equations = parseEquations lines'
      tokens = sum $ map calculateTokens equations
  return tokens

parseEquations :: [T.Text] -> [Equation]
parseEquations lines' = go lines' []
  where
    go [] acc = acc
    go (line:lines') acc =
      case stripPrefix "Button A: X+" (T.unpack line) of
        Just suffix ->
          case stripPrefix "Button B: X+" suffix of
            Just suffix' ->
              case stripPrefix "Prize: X=" suffix' of
                Just suffix'' ->
                  let a1 = read $ T.unpack $ T.takeWhile (/= ',') $ T.pack suffix
                      a2 = read $ T.unpack $ T.dropWhile (/= ',') $ T.pack suffix
                      b1 = read $ T.unpack $ T.takeWhile (/= ',') $ T.pack suffix'
                      b2 = read $ T.unpack $ T.dropWhile (/= ',') $ T.pack suffix'
                      c1 = read $ T.unpack $ T.takeWhile (/= ',') $ T.pack suffix''
                      c2 = read $ T.unpack $ T.dropWhile (/= ',') $ T.pack suffix''
                  in go lines' (Equation a1 a2 b1 b2 c1 c2 : acc)
                Nothing -> go lines' acc
            Nothing -> go lines' acc
        Nothing -> go lines' acc

calculateTokens :: Equation -> Int
calculateTokens equation@(Equation a1 a2 b1 b2 c1 c2) = 
  let xNumerator = b2 * c1 - b1 * c2
      yNumerator = a1 * c2 - a2 * c1
      denominator = a1 * b2 - a2 * b1
      x = xNumerator `div` denominator
      y = yNumerator `div` denominator
  in if denominator /= 0 && xNumerator `mod` denominator == 0 && yNumerator `mod` denominator == 0
       then 3 * x + y
       else 0

main :: IO ()
main = do
  result <- solution "data_test.txt"
  when (result /= 480) $ error "Assertion failed"
  solution "data.txt" >>= print