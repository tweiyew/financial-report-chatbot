import {
  Box,
  Button,
  Container,
  Grid,
  Heading,
  Input,
  Textarea,
  VStack,
  Text,
  Spinner,
  useToast,
  Divider,
  Avatar,
  Flex,
} from "@chakra-ui/react"
import { useState } from "react"

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)
  const toast = useToast()

  const handleSubmit = async () => {
    if (!file || !question.trim()) return

    setLoading(true)

    try {
      const formData = new FormData()
      formData.append("file", file)

      const uploadRes = await fetch("http://localhost:8000/upload-pdf", {
        method: "POST",
        body: formData,
      })

      const uploadData = await uploadRes.json()
      const file_id = uploadData.file_id

      const askRes = await fetch("http://localhost:8000/ask-question", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, file_id }),
      })

      const askData = await askRes.json()
      setAnswer(askData.answer || askData.error || "No response")
    } catch (err) {
      console.error(err)
      toast({
        title: "Server Error",
        description: "Unable to contact backend.",
        status: "error",
        duration: 3000,
        isClosable: true,
      })
    }

    setLoading(false)
  }

  return (
    <Box bg="#cbc6c6ff" minH="100vh" py={10}>
      <Container maxW="100xl">
        <Heading
          mb={10}
          size="xl"
          textAlign="center"
          color="#1F2937"
          fontWeight="extrabold"
        >
          PDF Q&A Dashboard
        </Heading>

        <Grid templateColumns={["1fr", null, "1fr 2fr"]} gap={8}>
          {/* Left Panel */}
          <VStack
            align="stretch"
            spacing={6}
            bg="white"
            p={6}
            borderRadius="xl"
            boxShadow="md"
          >
            <Box>
              <Heading size="md" mb={2} color="#1F2937">
                Upload PDF
              </Heading>
              <Text fontSize="sm" color="#6B7280" mb={3}>
                Select a document to analyse
              </Text>
              <Input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                variant="filled"
                bg="#F3F4F6"
              />
            </Box>

            <Box>
              <Heading size="md" mb={2} color="#1F2937">
                Ask a Question
              </Heading>
              <Text fontSize="sm" color="#6B7280" mb={3}>
                What do you want to know from the document?
              </Text>
              <Textarea
                placeholder="e.g., What are the main risks?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                resize="vertical"
                bg="#F3F4F6"
              />
              <Button
                mt={4}
                w="100%"
                size="lg"
                bgGradient="linear(to-r, #6366F1, #8B5CF6)"
                color="white"
                _hover={{ bgGradient: "linear(to-r, #4F46E5, #7C3AED)" }}
                onClick={handleSubmit}
                isDisabled={!file || !question.trim()}
              >
                Ask
              </Button>
            </Box>
          </VStack>

          {/* Right Panel */}
          <Box
            bg="white"
            p={6}
            borderRadius="xl"
            boxShadow="md"
            minH="350px"
          >
            <Heading size="md" mb={2} color="#1F2937">
              Response
            </Heading>
            <Text fontSize="sm" color="#6B7280" mb={4}>
              Powered by Gemini
            </Text>
            <Divider mb={4} />

            {loading ? (
              <Spinner size="xl" color="#6366F1" />
            ) : answer ? (
              <Box bg="#F3F4F6" p={5} borderRadius="lg">
                <Flex align="center" mb={3}>
                  <Avatar size="sm" name="Gemini AI" mr={2} />
                  <Text fontWeight="medium" color="#4B5563">
                    Gemini AI
                  </Text>
                </Flex>
                <Text whiteSpace="pre-wrap" color="#1F2937">
                  {answer}
                </Text>
              </Box>
            ) : (
              <Text color="#9CA3AF">Upload a PDF and ask a question to begin.</Text>
            )}
          </Box>
        </Grid>
      </Container>
    </Box>
  )
}

export default App
