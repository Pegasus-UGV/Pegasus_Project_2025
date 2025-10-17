#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class subscriber_node : public rclcpp::Node
{
    public:
        subscriber_node() : Node("Subscriber")
    {
        subscriber = this->create_subscription<std_msgs::msg::String>(
                "Hello_World_Topic", 10,
                std::bind(&subscriber_node::subscriber_callback, this, std::placeholders::_1));

        RCLCPP_INFO(get_logger(), "Subscriber Node Has Started");
    }

    private:
        void subscriber_callback(const std_msgs::msg::String::SharedPtr received_message)
        {
            RCLCPP_INFO(get_logger(), "%s", received_message->data.c_str());
        }

        // RCLCPP Config
        rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscriber;
};


int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<subscriber_node>();

    rclcpp::spin(node);
    rclcpp::shutdown();
}
